#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from struct import pack, unpack, error
from functools import reduce


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())

_OWEN_NAME = {'0': 0,  'A': 20, 'K': 40, 'U': 60,
              '1': 2,  'B': 22, 'L': 42, 'V': 62,
              '2': 4,  'C': 24, 'M': 44, 'W': 64,
              '3': 6,  'D': 26, 'N': 46, 'X': 66,
              '4': 8,  'E': 28, 'O': 48, 'Y': 68,
              '5': 10, 'F': 30, 'P': 50, 'Z': 70,
              '6': 12, 'G': 32, 'Q': 52, '-': 72,
              '7': 14, 'H': 34, 'R': 54, '_': 74,
              '8': 16, 'I': 36, 'S': 56, '/': 76,
              '9': 18, 'J': 38, 'T': 58, ' ': 78}

_OWEN_TYPE = {'F32': {'size': 4, 'pack': lambda value: pack('>f', value)[0:4],  'unpack': lambda value: unpack('>f', value[0:4])[0]},
              'F24': {'size': 3, 'pack': lambda value: pack('>f', value)[0:3],  'unpack': lambda value: unpack('>f', value[0:3] + b'\x00')[0]},
              'U16': {'size': 2, 'pack': lambda value: pack('>H', value)[0:2],  'unpack': lambda value: unpack('>H', value[0:2])[0]},
              'I16': {'size': 2, 'pack': lambda value: pack('>h', value)[0:2],  'unpack': lambda value: unpack('>h', value[0:2])[0]},
              'U8':  {'size': 1, 'pack': lambda value: pack('>B', value)[0:1],  'unpack': lambda value: unpack('>B', value[0:1])[0]},
              'I8':  {'size': 1, 'pack': lambda value: pack('>b', value)[0:1],  'unpack': lambda value: unpack('>b', value[0:1])[0]},
              'U24': {'size': 3, 'pack': lambda value: pack('>BH', value)[0:3], 'unpack': lambda value: unpack('>BH', value[0:3])},     # для N.err
              'STR': {'size': 8, 'pack': lambda value: value[::-1],             'unpack': lambda value: value[::-1]}}


class Owen(object):
    ''' Класс для работы по протоколу ОВЕН '''

    addrLen = 8     # длина адреса в битах (8 или 11)

    def __init__(self, client, unit):
        self.client = client
        self.unit = unit

        self._data_size = 0

    def __del__(self):
        if self.client.is_open:
            self.client.close()
            self.client = None

    def __repr__(self):
        return ("Owen(client={}, unit={})".format(self.client, self.unit))

# Функции расчета хеш-суммы

    def _fastCalc(self, value, tmp, n):
        for _ in range(n):
            value &= 0xFF
            if (value ^ tmp>>8) & 0x80:
                tmp <<= 1
                tmp ^= 0x8F57
            else:
                tmp <<= 1
            tmp &= 0xFFFF
            value <<= 1

        return tmp

    def _owenCRC16(self, packet):
        return reduce(lambda crc, val: self._fastCalc(val, crc, 8), packet, 0)

    def _owenHash(self, packet):
        return reduce(lambda crc, val: self._fastCalc(val<<1, crc, 7), packet, 0)

    def _name2hash(self, name):
        owen_name = reduce(lambda x, ch: x[:-1] + [x[-1]+1] if ch == '.'
                            else x + [_OWEN_NAME[ch]], name.upper(), [])
        owen_name += [_OWEN_NAME[' ']] * (4-len(owen_name))

        return self._owenHash(owen_name)

# Функции упаковки/распаковки пакетов

    def _bytes2ascii(self, buff):
        ascii = [chr(71 + (num>>4 & 0xF)) + chr(71 + (num & 0xF)) for num in buff]
        return '#' + "".join(ascii) + '\r'

    def _ascii2bytes(self, buff):
        return [ord(buff[i])-71 << 4 | ord(buff[i+1])-71 & 0xF
                for i in range(1, len(buff)-1, 2)]

# Функции упаковки/распаковки данных

    def _packValue(self, frmt, value):
        return _OWEN_TYPE[frmt]['pack'](value)

    def _unpackValue(self, frmt, buff):
        if buff:
            try:
                return _OWEN_TYPE[frmt]['unpack'](buff)
            except error:
                errcode = _OWEN_TYPE['U8']['unpack'](buff)
                _logger.error("OwenProtocolError: error={:02X}".format(errcode))

# Функции формирования/разбора пакетов

    def _makepacket(self, address, flag, cmd, data):
        if self.addrLen == 8:
            addr0 = address & 0xFF
            addr1 = 0
        elif self.addrLen == 11:
            addr0 = address>>3 & 0xFF
            addr1 = (address & 0x07) << 5
        else:
            raise ValueError("OwenProtocolError: Address length must be 8 or 11")

        packet = [addr0, addr1 + (flag << 4) + len(data), cmd>>8 & 0xFF, cmd & 0xFF] + data
        crc = self._owenCRC16(packet)

        _logger.debug("Send param = address:{}, flag:{}, size:{}, cmd:{:04X}, "
                      "data:{}, crc:{:04X}".format(address, flag, len(data), cmd, data, crc))

        ret = self._bytes2ascii(packet + [crc>>8 & 0xFF, crc & 0xFF])

        return ret.encode("ascii")

    def _parse_resp(self, message, name=None):
        message = message.decode("ascii")
        if not message or message[0] != "#" or message[-1] != "\r":
            _logger.error("OwenProtocolError: Wrong readed message format")
            return None

        frame = self._ascii2bytes(message)
        # ВНИМАНИЕ: невозможно отличить 11-битные адреса, кратные 8, от 8-битных
        address = frame[0]<<3 | frame[1]>>5 & 0xff if frame[1] & 0xe0 else frame[0]
        flag = frame[1] & 0x10
        size = frame[1] & 0xF
        cmd = (frame[2] << 8) + frame[3]
        data = frame[4: 4+size]
        crc = (frame[-2] << 8) + frame[-1]

        _logger.debug("Recv param = address:{}, flag:{}, size:{}, cmd:{:04X}, "
                      "data:{}, crc:{:04X}".format(address, flag, size, cmd, data, crc))

        if self._owenCRC16(frame[0:-2]) != crc:
            _logger.error("OwenProtocolError: Checksumm mismatch")
            return None
        elif name != "N.ERR" and cmd == 0x0233:
            _logger.error("OwenProtocolError: error={:02X}, hash={:02X}{:02X}".format(*data))
            return None

        return bytearray(data)

# Функции обмена с прибором

    def _getPingPong(self, flag, name, index, data=None):
        nhash = self._name2hash(name)
        if data is None: data = []
        if index is not None:
            data.extend([index>>8 & 0xFF, index & 0xFF])
            self._data_size += 2

        packet = self._makepacket(self.unit, flag, nhash, data)

        _logger.debug("Send frame = {!r}, len={}".format(packet, len(packet)))

        self.client.reset_input_buffer()
        self.client.reset_output_buffer()

        self.client.write(packet)
        waitbytes = 2 + 6*2 + 2*self._data_size
        answer = self.client.read(waitbytes)

        _logger.debug("Recv frame = {!r}, len={}".format(answer, len(answer)))

        return answer==packet or self._parse_resp(answer, name)

# Функции чтения/записи данных

    def getParam(self, frmt, name, index=None):
        self._data_size = _OWEN_TYPE[frmt]['size']
        data = self._getPingPong(1, name, index)
        return self._unpackValue(frmt, data)

    def setParam(self, frmt, name, index=None, value=None):
        data = list(bytearray(self._packValue(frmt, value))) if value is not None else []
        self._data_size = len(data)
        return self._getPingPong(0, name, index, data)


__all__ = [ "Owen" ]
