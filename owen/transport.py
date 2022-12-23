#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep
from serial import Serial, SerialException
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.version import version
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

from .protocol import Owen

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class BaseTransport(object):
    """ Базовый класс транспорта для взаимодействия с устройством """

    def __init__(self, *args, **kwargs):
        self._socket = None

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._socket)

    def __del__(self):
        self.close()

    def connect(self):
        raise NotImplementedError()

    def close(self):
        if self._socket:
            self._socket.close()
        self._socket = None

    def get_param(self, name, index=None):
        raise NotImplementedError()

    def set_param(self, name, index=None, value=None):
        raise NotImplementedError()

    def check_param(self, dev, name, index, value=None):
        if not index:
            if None in dev['index']: index = None
            elif 0 in dev['index']:  index = 0

        if index not in dev['index']:
            raise ValueError("{}: Parameter '{}' not supported index {}".
                             format(type(self).__name__, name, index))
        if value is not None:
            if value < dev['min'] or value > dev['max']:
                raise ValueError("{}: Parameter '{}' out of range ({}, {}) value {}".
                                 format(type(self).__name__, name, dev['min'],
                                        dev['max'], value))
        return index


class OwenSerialTransport(BaseTransport):
    """ Класс транспорта для взаимодействия с устройством по протоколу ОВЕН """

    device = None
    unit = None
    addr_len_8 = True

    def __init__(self, *args, **kwargs):
        super(OwenSerialTransport, self).__init__(args, kwargs)

        self._owen = None
        self._socket = None
        self._args = args
        self._kwargs = kwargs

    def connect(self):
        if self._socket:
            return True

        try:
            self._socket = Serial(*self._args, **self._kwargs)
            self._owen = Owen(self._socket, self.unit)
            self._owen.addr_len_8 = self.addr_len_8
        except SerialException as msg:
            _logger.error(msg)
            self.close()

        return self._socket is not None

    def get_param(self, name, index=None):
        dev = self.device['Owen'][name]
        index = self.check_param(dev, name, index)

        return self._owen.get_param(dev['type'], name, index)

    def set_param(self, name, index=None, value=None):
        dev = self.device['Owen'][name]
        index = self.check_param(dev, name, index, value)

        return self._owen.set_param(dev['type'], name, index, value)


class OwenModbusTransport(BaseTransport):
    """ Класс транспорта для взаимодействия с устройством по протоколу Modbus """

    device = None
    unit = None

    def __init__(self, *args, **kwargs):
        super(OwenModbusTransport, self).__init__(args, kwargs)

        socket = kwargs.get("socket", None)
        if socket is not None:
            self._socket = socket
        else:
            self._socket = ModbusSerialClient(*args, **kwargs)

    def connect(self):
        return self._socket.connect()

    def _error_check(self, name, retcode):
        if not retcode:         # for python2 and pymodbus v1.3.0
            _logger.error("Unit %d called '%s' with error: "
                          "Modbus Error: [Input/Output] No Response received "
                          "from the remote unit", self.unit, name)
        elif isinstance(retcode, (ModbusException, ExceptionResponse)):
            _logger.error("Unit %d called '%s' with error: %s", self.unit, name, retcode)
        else:
            return True

    def _get(self, dev, name, index):
        index = self.check_param(dev, name, index)

        if dev['type'] == "STR": count = 4
        elif dev['type'] in ["I32", "U32", "F32"]: count = 2
        else: count = 1

        result = self._socket.read_holding_registers(address=dev['index'][index],
                                                     count=count,
                                                     unit=self.unit)
        if self._error_check(name, result):
            if int(version.short()[0]) > 1:
                decoder = BinaryPayloadDecoder.fromRegisters(registers=result.registers,
                                                             byteorder=Endian.Big,
                                                             wordorder=Endian.Little)
            else:
                decoder = BinaryPayloadDecoder.fromRegisters(registers=result.registers,
                                                             endian=Endian.Big)
            if dev['type'] == "U16":   return decoder.decode_16bit_uint()
            elif dev['type'] == "I16": return decoder.decode_16bit_int()
            elif dev['type'] == "U32": return decoder.decode_32bit_uint()
            elif dev['type'] == "I32": return decoder.decode_32bit_int()
            elif dev['type'] == "F32": return decoder.decode_32bit_float()
            elif dev['type'] == "STR": return decoder.decode_string(8)

    def get_param(self, name, index=None):
        dev = self.device['Modbus'][name]

        if dev['dp']:
            _dev = self.device['Modbus'][dev['dp']]
            dp = self._get(_dev, dev['dp'], index)
            ret = self._get(dev, name, index)/10.0**dp
        else:
            ret = self._get(dev, name, index)

        prec = dev['precision']
        return ret if not prec else ret/10.0**prec

    def set_param(self, name, index=None, value=None):
        dev = self.device['Modbus'][name]

        index = self.check_param(dev, name, index, value)

        if dev['dp']:
            _dev = self.device['Modbus'][dev['dp']]
            dp = self._get(_dev, dev['dp'], index)
            value *= 10.0**dp
            sleep(0.05)     # ???

        prec = dev['precision']
        value = value if not prec else value * 10.0**prec

        if int(version.short()[0]) > 1:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                           wordorder=Endian.Little)
        else:
            builder = BinaryPayloadBuilder(endian=Endian.Big)

        if dev['type'] == "I16":   builder.add_16bit_int(int(value))
        elif dev['type'] == "U16": builder.add_16bit_uint(int(value))
        elif dev['type'] == "I32": builder.add_32bit_int(int(value))
        elif dev['type'] == "U32": builder.add_32bit_uint(int(value))
        elif dev['type'] == "F32": builder.add_32bit_float(float(value))
        elif dev['type'] == "STR": builder.add_string(str(value))

        result = self._socket.write_registers(address=dev['index'][index],
                                              values=builder.build(),
                                              skip_encode=True,
                                              unit=self.unit)
        return self._error_check(name, result)


__all__ = [ "OwenSerialTransport", "OwenModbusTransport" ]
