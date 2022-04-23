#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.version import version
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

from .protocol import Owen

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class OwenSerialClient(object):
    addr_len = 8

    def __init__(self, transport, device, unit):
        self._transport = transport
        if not self._transport.is_open:
            raise Exception("OwenSerialClient Error: Socket not connected")

        self._device = device
        self._unit = unit

        self._owen = Owen(self._transport, self._unit)
        self._owen.addrLen = self.addr_len

    def __repr__(self):
        return ("OwenSerialClient(transport={}, unit={})".
                 format(self._transport, self._unit))

    def __del__(self):
        if self._transport.is_open:
            self._transport.close()

    def _checkParam(self, name, index, value=None):
        if not index:
            index = self._dev['index'][0]

        if index not in self._dev['index']:
            raise KeyError("OwenSerialClient Error: This index not supported")

        if value is not None:
            if value < self._dev['min'] or value > self._dev['max']:
                raise ValueError("OwenSerialClient Error: Parameter '{}' "
                                 "out of range ({}, {})".
                                 format(name, self._dev['min'], self._dev['max']))
        return index

    def getParam(self, name, index=None):
        name = name.upper()
        self._dev = self._device['Owen'][name]
        index = self._checkParam(name, index)

        return self._owen.getParam(self._dev['type'], name, index)

    def setParam(self, name, index=None, value=None):
        name = name.upper()
        self._dev = self._device['Owen'][name]
        index = self._checkParam(name, index, value)

        return self._owen.setParam(self._dev['type'], name, index, value)


class OwenModbusClient(object):
    def __init__(self, transport, device, unit):
        self._transport = transport
        if not self._transport.connect():
            raise Exception("OwenModbusClient Error: Socket not connected")

        self._device = device
        self._unit = unit

    def __repr__(self):
        return ("OwenModbusClient(transport={}, unit={})".
                 format(self._transport, self._unit))

    def __del__(self):
        if self._transport:
            self._transport.close()

    def _errorCheck(self, name, retcode):
        if not retcode:         # for python2 and pymodbus v1.3.0
            _logger.error("Unit {} called '{}' with error: "
                          "Modbus Error: [Input/Output] No Response received "
                          "from the remote unit".format(self._unit, name))
        elif isinstance(retcode, (ModbusException, ExceptionResponse)):
            _logger.error("Unit {} called '{}' with error: {}".
                           format(self._unit, name, retcode))
        else:
            return True

    def _checkParam(self, name, index, value=None):
        if not index:
            if None in self._dev['index']: index = None
            elif 0 in self._dev['index']:  index = 0

        if index not in self._dev['index']:
            raise KeyError("OwenModbusClient Error: This index not supported")

        if value is not None:
            if value < self._dev['min'] or value > self._dev['max']:
                raise ValueError("OwenModbusClient Error: Parameter '{}' "
                                 "out of range ({}, {})".
                                 format(name, self._dev['min'], self._dev['max']))
        return index

    def getParam(self, name, index=None):
        name = name.upper()
        self._dev = self._device['Modbus'][name]

        index = self._checkParam(name, index)

        if self._dev['type'] == "STR": count = 4
        elif self._dev['type'] in ["I32", "U32", "F32"]: count = 2
        else: count = 1

        result = self._transport.read_holding_registers(address=self._dev['index'][index],
                                                        count=count,
                                                        unit=self._unit)
        if self._errorCheck(name, result):
            if int(version.short()[0]) > 1:
                decoder = BinaryPayloadDecoder.fromRegisters(registers=result.registers,
                                                             byteorder=Endian.Big,
                                                             wordorder=Endian.Little)
            else:
                decoder = BinaryPayloadDecoder.fromRegisters(registers=result.registers,
                                                             endian=Endian.Big)
            if self._dev['type'] == "U16":   return decoder.decode_16bit_uint()
            elif self._dev['type'] == "I16": return decoder.decode_16bit_int()
            elif self._dev['type'] == "U32": return decoder.decode_32bit_uint()
            elif self._dev['type'] == "I32": return decoder.decode_32bit_int()
            elif self._dev['type'] == "F32": return decoder.decode_32bit_float()
            elif self._dev['type'] == "STR": return decoder.decode_string(8)

    def setParam(self, name, index=None, value=None):
        name = name.upper()
        self._dev = self._device['Modbus'][name]

        index = self._checkParam(name, index, value)

        if int(version.short()[0]) > 1:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                           wordorder=Endian.Little)
        else:
            builder = BinaryPayloadBuilder(endian=Endian.Big)

        if self._dev['type'] == "I16":   builder.add_16bit_int(int(value))
        elif self._dev['type'] == "U16": builder.add_16bit_uint(int(value))
        elif self._dev['type'] == "I32": builder.add_32bit_int(int(value))
        elif self._dev['type'] == "U32": builder.add_32bit_uint(int(value))
        elif self._dev['type'] == "F32": builder.add_32bit_float(float(value))
        elif self._dev['type'] == "STR": builder.add_string(str(value))

        payload = builder.build()

        result = self._transport.write_registers(address=self._dev['index'][index],
                                                 values=payload,
                                                 skip_encode=True,
                                                 unit=self._unit)
        return self._errorCheck(name, result)


__all__ = [ "OwenSerialClient", "OwenModbusClient" ]
