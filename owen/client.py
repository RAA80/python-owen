#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from operator import truediv, mul
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

from .protocol import Owen

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class BaseClient(object):
    """ Базовый класс клиента для взаимодействия с устройством """

    def __init__(self, transport, device, unit):
        self.device = device
        self.unit = unit
        self.socket = transport

        self.connect()

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.socket, self.unit)

    def __del__(self):
        self.close()

    def connect(self):
        """ Подключение к удаленному устройству """

        raise NotImplementedError()

    def close(self):
        """ Закрытие соединения """

        if self.socket:
            self.socket.close()
        self.socket = None

    def get_param(self, name, index=None):
        """ Чтение данных из устройства """

        raise NotImplementedError()

    def set_param(self, name, index=None, value=None):
        """ Запись данных в устройство """

        raise NotImplementedError()

    def check_param(self, proto, name, index, value=None):
        """ Проверка введенных данных """

        dev = self.device[proto][name]

        if not index:
            index = None if None in dev['index'] else 0

        if index not in dev['index']:
            raise ValueError("Parameter '{}' not in supported indexes {} index '{}'".
                             format(name, tuple(dev["index"]), index))
        if (value is not None) and (value < dev['min'] or value > dev['max']):
            raise ValueError("Parameter '{}' out of range ({}, {}) value '{}'".
                             format(name, dev['min'], dev['max'], value))
        return dev, index


class OwenSerialClient(BaseClient):
    """ Класс клиента для взаимодействия с устройством по протоколу ОВЕН """

    def __init__(self, transport, device, unit, addr_len_8=True):
        self.addr_len_8 = addr_len_8
        self._owen = None

        super(OwenSerialClient, self).__init__(transport, device, unit)

    def connect(self):
        if self.socket.is_open:
            self._owen = Owen(self.socket, self.unit)
            self._owen.addr_len_8 = self.addr_len_8
            return True

    def get_param(self, name, index=None):
        dev, index = self.check_param('Owen', name, index)
        return self._owen.get_param(dev['type'], name, index)

    def set_param(self, name, index=None, value=None):
        dev, index = self.check_param('Owen', name, index, value)
        return self._owen.set_param(dev['type'], name, index, value)


class OwenModbusClient(BaseClient):
    """ Класс клиента для взаимодействия с устройством по протоколу Modbus """

    def __init__(self, transport, device, unit):
        super(OwenModbusClient, self).__init__(transport, device, unit)

    def connect(self):
        return self.socket.connect()

    def _error_check(self, name, retcode):
        if not retcode:         # for python2 and pymodbus v1.3.0
            _logger.error("Unit %d called '%s' with error: "
                          "Modbus Error: [Input/Output] No Response received "
                          "from the remote unit", self.unit, name)
        elif isinstance(retcode, (ModbusException, ExceptionResponse)):
            _logger.error("Unit %d called '%s' with error: %s", self.unit, name, retcode)
        else:
            return True

    def _read(self, dev, name, index):
        count = {"U16": 1, "I16": 1, "U32": 2, "I32": 2, "F32": 2, "STR": 4
                }[dev['type']]
        result = self.socket.read_holding_registers(address=dev['index'][index],
                                                    count=count,
                                                    unit=self.unit)
        if self._error_check(name, result):
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)

            if dev['type'] == "U16":   return decoder.decode_16bit_uint()
            elif dev['type'] == "I16": return decoder.decode_16bit_int()
            elif dev['type'] == "U32": return decoder.decode_32bit_uint()
            elif dev['type'] == "I32": return decoder.decode_32bit_int()
            elif dev['type'] == "F32": return decoder.decode_32bit_float()
            elif dev['type'] == "STR": return decoder.decode_string(8)

    def _modify_value(self, func, dev, index, value):
        if dev['dp']:
            dp_dev = self.device['Modbus'][dev['dp']]
            dp = self._read(dp_dev, dev['dp'], index)
            value = func(value, 10.0**dp)

        prec = dev['precision']
        return func(value, 10.0**prec) if prec else value

    def get_param(self, name, index=None):
        dev, index = self.check_param('Modbus', name, index)
        value = self._read(dev, name, index)
        return self._modify_value(truediv, dev, index, value)

    def set_param(self, name, index=None, value=None):
        dev, index = self.check_param('Modbus', name, index, value)
        value = self._modify_value(mul, dev, index, value)

        builder = BinaryPayloadBuilder(None, Endian.Big)

        if dev['type'] == "I16":   builder.add_16bit_int(int(value))
        elif dev['type'] == "U16": builder.add_16bit_uint(int(value))
        elif dev['type'] == "I32": builder.add_32bit_int(int(value))
        elif dev['type'] == "U32": builder.add_32bit_uint(int(value))
        elif dev['type'] == "F32": builder.add_32bit_float(float(value))
        elif dev['type'] == "STR": builder.add_string(str(value))

        result = self.socket.write_registers(address=dev['index'][index],
                                             values=builder.build(),
                                             skip_encode=True,
                                             unit=self.unit)
        return self._error_check(name, result)


__all__ = [ "OwenSerialClient", "OwenModbusClient" ]
