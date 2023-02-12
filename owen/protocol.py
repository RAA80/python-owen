#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from struct import pack, unpack, error
from functools import reduce


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())

_OWEN_NAME = {'0': 0,  '1': 2,  '2': 4,  '3': 6,  '4': 8,
              '5': 10, '6': 12, '7': 14, '8': 16, '9': 18,
              'A': 20, 'B': 22, 'C': 24, 'D': 26, 'E': 28,
              'F': 30, 'G': 32, 'H': 34, 'I': 36, 'J': 38,
              'K': 40, 'L': 42, 'M': 44, 'N': 46, 'O': 48,
              'P': 50, 'Q': 52, 'R': 54, 'S': 56, 'T': 58,
              'U': 60, 'V': 62, 'W': 64, 'X': 66, 'Y': 68,
              'Z': 70, '-': 72, '_': 74, '/': 76, ' ': 78}

_OWEN_TYPE = {'F32': {'pack': lambda value: pack('>f', value)[0:4],  'unpack': lambda value: unpack('>f', value[0:4])[0]},
              'F24': {'pack': lambda value: pack('>f', value)[0:3],  'unpack': lambda value: unpack('>f', value[0:3] + b'\x00')[0]},
              'U16': {'pack': lambda value: pack('>H', value)[0:2],  'unpack': lambda value: unpack('>H', value[0:2])[0]},
              'I16': {'pack': lambda value: pack('>h', value)[0:2],  'unpack': lambda value: unpack('>h', value[0:2])[0]},
              'U8':  {'pack': lambda value: pack('>B', value)[0:1],  'unpack': lambda value: unpack('>B', value[0:1])[0]},
              'I8':  {'pack': lambda value: pack('>b', value)[0:1],  'unpack': lambda value: unpack('>b', value[0:1])[0]},
              'U24': {'pack': lambda value: pack('>BH', value)[0:3], 'unpack': lambda value: unpack('>BH', value[0:3])},     # для N.err
              'STR': {'pack': lambda value: value[::-1],             'unpack': lambda value: value[::-1]}}


class Owen(object):
    ''' Класс, описывающий протокол ОВЕН '''

    addr_len_8 = True    # длина адреса в битах: True=8, False=11

    def __init__(self, client, unit):
        self.client = client
        self.unit = unit

    def __repr__(self):
        return "Owen(client={}, unit={})".format(self.client, self.unit)

    def _fast_calc(self, value, crc, bits):
        """ Вычисление значения полинома """

        return reduce(lambda crc, i: crc<<1 & 0xFFFF ^ (0x8F57
                      if (value<<i ^ crc>>8) & 0x80 else 0), range(bits), crc)

    def _owen_crc16(self, packet):
        """ Вычисление контрольной суммы """

        return reduce(lambda crc, val: self._fast_calc(val, crc, 8), packet, 0)

    def _owen_hash(self, packet):
        """ Вычисление hash-функции """

        return reduce(lambda crc, val: self._fast_calc(val<<1, crc, 7), packet, 0)

    def _name2hash(self, name):
        """ Преобразование локального идентификатора в двоичный вид """

        owen_name = reduce(lambda x, ch: x[:-1] + [x[-1]+1] if ch == '.'
                           else x + [_OWEN_NAME[ch]], name.upper(), [])
        owen_name += [_OWEN_NAME[' ']] * (4 - len(owen_name))

        return self._owen_hash(owen_name)

    def _bytes2ascii(self, buff):
        """ Преобразование пакета из бинарного вида в строковый """

        chars = [chr(71 + (num>>4 & 0xF)) + chr(71 + (num & 0xF)) for num in buff]
        return ('#' + "".join(chars) + '\r').encode("ascii")

    def _ascii2bytes(self, buff):
        """ Преобразование пакета из строкового вида в бинарный """

        return [ord(i)-71 << 4 | ord(j)-71 & 0xF
                for i,j in zip(*[iter(buff[1:-1])]*2)]

    def _pack_value(self, frmt, value):
        """ Упаковка данных """

        if value is not None:
            return list(bytearray(_OWEN_TYPE[frmt]['pack'](value)))

    def _unpack_value(self, frmt, buff):
        """ Распаковка данных """

        if buff:
            try:
                return _OWEN_TYPE[frmt]['unpack'](buff)
            except error:
                errcode = _OWEN_TYPE['U8']['unpack'](buff)
                _logger.error("OwenProtocolError: error=%02X", errcode)

    def _make_packet(self, flag, cmd, index, data):
        """ Формирование пакета для записи """

        addr0, addr1 = (self.unit & 0xFF, 0) if self.addr_len_8 \
                       else (self.unit>>3 & 0xFF, (self.unit & 0x07) << 5)
        if data is None:
            data = []
        if index is not None:
            data.extend([index>>8 & 0xFF, index & 0xFF])

        packet = [addr0, addr1 + (flag << 4) + len(data), cmd>>8 & 0xFF, cmd & 0xFF] + data
        crc = self._owen_crc16(packet)

        _logger.debug("Send param: address=%d, flag=%d, size=%d, cmd=%04X, "
                      "data=%s, crc=%04X", self.unit, flag, len(data), cmd, data, crc)

        return self._bytes2ascii(packet + [crc>>8 & 0xFF, crc & 0xFF])

    def _parse_response(self, answer, name):
        """ Расшифровка прочитанного пакета """

        answer = answer.decode("ascii")
        if not answer or answer[0] != "#" or answer[-1] != "\r":
            _logger.error("OwenProtocolError: Wrong readed message format")
            return None

        frame = self._ascii2bytes(answer)

        address = frame[0] if self.addr_len_8 else frame[0]<<3 | frame[1]>>5
        flag = frame[1]>>4 & 1
        size = frame[1] & 0xF
        cmd = (frame[2] << 8) + frame[3]
        data = frame[4: 4 + size]
        crc = (frame[-2] << 8) + frame[-1]

        _logger.debug("Recv param: address=%d, flag=%d, size=%d, cmd=%04X, "
                      "data=%s, crc=%04X", address, flag, size, cmd, data, crc)

        if self._owen_crc16(frame[0:-2]) != crc:
            _logger.error("OwenProtocolError: Checksumm mismatch")
            return None
        if name != "N.ERR" and cmd == 0x0233:
            _logger.error("OwenProtocolError: error=%02X, hash=%02X%02X", *data)
            return None

        return bytearray(data)

    def _data_exchange(self, flag, name, index, data=None):
        """ Подготовка данных для записи """

        cmd = self._name2hash(name)
        packet = self._make_packet(flag, cmd, index, data)

        _logger.debug("Send frame: %r, size=%d", packet, len(packet))
        answer = self._get_ping_pong(packet)
        _logger.debug("Recv frame: %r, size=%d", answer, len(answer))

        return answer == packet or self._parse_response(answer, name)

    def _get_ping_pong(self, packet):
        """ Обмен данными с устройством через порт """

        self.client.reset_input_buffer()
        self.client.reset_output_buffer()

        self.client.write(packet)
        return self.client.read_until(b'\r')

    def get_param(self, frmt, name, index=None):
        """ Чтение данных из устройства """

        data = self._data_exchange(1, name, index)
        return self._unpack_value(frmt, data)

    def set_param(self, frmt, name, index=None, value=None):
        """ Запись данных в устройство """

        data = self._pack_value(frmt, value) or []
        return self._data_exchange(0, name, index, data)


__all__ = [ "Owen" ]
