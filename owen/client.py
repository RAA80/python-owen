#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from operator import mul, truediv

from pymodbus.constants import Endian
from pymodbus.exceptions import ModbusException
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.pdu import ExceptionResponse

from .protocol import Owen

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class ClientMixin(object):
    """ Класс-примесь клиента. """

    def __init__(self, transport, device, unit):
        self.device = device
        self.unit = unit
        self.socket = transport

        self.connect()

    def __repr__(self):
        return "{}(transport={}, unit={})".format(type(self).__name__,
                                                  self.socket, self.unit)

    def __del__(self):
        self.close()

    def connect(self):
        """ Подключение к удаленному устройству (должен быть переопределен). """

    def close(self):
        """ Закрытие соединения. """

        if self.socket:
            self.socket.close()
        self.socket = None

    def check_index(self, name, dev, index):
        """ Проверка индекса. """

        if not index:
            index = None if None in dev["index"] else 0
        if index not in dev["index"]:
            msg = "'{}' does not support index '{}'".format(name, index)
            raise ValueError(msg)

        return index

    def check_value(self, name, dev, value):
        """ Проверка данных. """

        if all([value is None, dev["min"] is None, dev["max"] is None]):
            return value
        if all([value is None, dev["min"] is not None, dev["max"] is not None]) or \
           all([value is not None, dev["min"] is None, dev["max"] is None]) or \
           all([value is not None, dev["min"] > value]) or \
           all([value is not None, dev["max"] < value]):
            msg = "An '{}' value of '{}' is out of range".format(name, value)
            raise ValueError(msg)

        return value


class OwenSerialClient(ClientMixin):
    """ Класс клиента для взаимодействия с устройством по протоколу ОВЕН. """

    def __init__(self, transport, device, unit, addr_len_8=True):
        self._owen = Owen(unit, addr_len_8)     # длина адреса в битах: True=8, False=11

        super(OwenSerialClient, self).__init__(transport, device, unit)

    def connect(self):
        """ Подключение к удаленному устройству. """

        return self.socket.is_open

    def bus_exchange(self, packet):
        """ Обмен по интерфейсу. """

        self.socket.reset_input_buffer()
        self.socket.reset_output_buffer()

        self.socket.write(packet)
        return self.socket.read_until(b"\r")

    def send_message(self, flag, name, index, data=None):
        """ Подготовка данных для обмена. """

        packet = self._owen.make_packet(flag, name, index, data)
        answer = self.bus_exchange(packet)
        return self._owen.parse_response(packet, answer)

    def get_param(self, name, index=None):
        """ Чтение данных из устройства. """

        dev = self.device["Owen"][name.upper()]
        index = self.check_index(name, dev, index)
        result = self.send_message(1, name, index)
        return self._owen.unpack_value(dev["type"], result)

    def set_param(self, name, index=None, value=None):
        """ Запись данных в устройство. """

        dev = self.device["Owen"][name.upper()]
        index = self.check_index(name, dev, index)
        value = self.check_value(name, dev, value)
        data = self._owen.pack_value(dev["type"], value)
        return self.send_message(0, name, index, data)


class OwenModbusClient(ClientMixin):
    """ Класс клиента для взаимодействия с устройством по протоколу Modbus. """

    def __init__(self, transport, device, unit):
        super(OwenModbusClient, self).__init__(transport, device, unit)

    def connect(self):
        """ Подключение к удаленному устройству. """

        return self.socket.connect()

    def check_error(self, retcode):
        """ Проверка возвращаемого значения на ошибку. """

        if not isinstance(retcode, (ModbusException, ExceptionResponse, type(None))):
            return True
        _logger.error("Unit %d return %s", self.unit, retcode)

    def _read(self, dev, index):
        """ Чтение данных из регистра Modbus. """

        count = {"U16": 1, "I16": 1, "U32": 2, "I32": 2, "F32": 2, "STR": 4,
                }[dev["type"]]
        result = self.socket.read_holding_registers(address=dev["index"][index],
                                                    count=count,
                                                    unit=self.unit)
        if self.check_error(result):
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)
            return {"U16": decoder.decode_16bit_uint,
                    "I16": decoder.decode_16bit_int,
                    "U32": decoder.decode_32bit_uint,
                    "I32": decoder.decode_32bit_int,
                    "F32": decoder.decode_32bit_float,
                    "STR": lambda: decoder.decode_string(8),
                   }[dev["type"]]()

    def modify_value(self, func, dev, index, value):
        """ Преобразование значения к нужной точности. """

        if dev["dp"]:
            dp_dev = self.device["Modbus"][dev["dp"]]
            dp = self._read(dp_dev, index)
            value = func(value, 10.0**dp)

        prec = dev["precision"]
        return func(value, 10.0**prec) if prec else value

    def get_param(self, name, index=None):
        """ Чтение данных из устройства. """

        dev = self.device["Modbus"][name.upper()]
        index = self.check_index(name, dev, index)
        value = self._read(dev, index)
        return None if value is None else self.modify_value(truediv, dev, index, value)

    def set_param(self, name, index=None, value=None):
        """ Запись данных в устройство. """

        dev = self.device["Modbus"][name.upper()]
        index = self.check_index(name, dev, index)
        value = self.check_value(name, dev, value)
        value = self.modify_value(mul, dev, index, value)

        builder = BinaryPayloadBuilder(None, Endian.Big)
        {"U16": lambda value: builder.add_16bit_uint(int(value)),
         "I16": lambda value: builder.add_16bit_int(int(value)),
         "U32": lambda value: builder.add_32bit_uint(int(value)),
         "I32": lambda value: builder.add_32bit_int(int(value)),
         "F32": lambda value: builder.add_32bit_float(float(value)),
         "STR": lambda value: builder.add_string(str(value)),
        }[dev["type"]](value)

        result = self.socket.write_registers(address=dev["index"][index],
                                             values=builder.build(),
                                             skip_encode=True,
                                             unit=self.unit)
        return self.check_error(result)


__all__ = ["OwenSerialClient", "OwenModbusClient"]
