#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from functools import reduce
from struct import error

from .converter import (pack_f24, pack_f32, pack_f32t, pack_i8, pack_i16,
                        pack_sdot, pack_str, pack_u8, pack_u16, pack_u24,
                        unpack_f24, unpack_f32, unpack_f32t, unpack_i8,
                        unpack_i16, unpack_sdot, unpack_str, unpack_u8,
                        unpack_u16, unpack_u24)

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


_OWEN_NAME = {"0": 0,  "1": 2,  "2": 4,  "3": 6,  "4": 8,
              "5": 10, "6": 12, "7": 14, "8": 16, "9": 18,
              "A": 20, "B": 22, "C": 24, "D": 26, "E": 28,
              "F": 30, "G": 32, "H": 34, "I": 36, "J": 38,
              "K": 40, "L": 42, "M": 44, "N": 46, "O": 48,
              "P": 50, "Q": 52, "R": 54, "S": 56, "T": 58,
              "U": 60, "V": 62, "W": 64, "X": 66, "Y": 68,
              "Z": 70, "-": 72, "_": 74, "/": 76, " ": 78}

_OWEN_TYPE = {"F32+T": {"pack": pack_f32t, "unpack": unpack_f32t},
              "SDOT":  {"pack": pack_sdot, "unpack": unpack_sdot},
              "F32":   {"pack": pack_f32,  "unpack": unpack_f32},
              "F24":   {"pack": pack_f24,  "unpack": unpack_f24},
              "U16":   {"pack": pack_u16,  "unpack": unpack_u16},
              "I16":   {"pack": pack_i16,  "unpack": unpack_i16},
              "U8":    {"pack": pack_u8,   "unpack": unpack_u8},
              "I8":    {"pack": pack_i8,   "unpack": unpack_i8},
              "U24":   {"pack": pack_u24,  "unpack": unpack_u24},   # для N.err
              "STR":   {"pack": pack_str,  "unpack": unpack_str}}


class Owen(object):
    """ Класс, описывающий протокол ОВЕН. """

    def __init__(self, unit, addr_len_8=True):
        self.unit = unit
        self.addr_len_8 = addr_len_8

    def __repr__(self):
        return "Owen(unit={}, addr_len_8={}".format(self.unit, self.addr_len_8)

    @staticmethod
    def fast_calc(value, crc, bits):
        """ Вычисление значения полинома. """

        return reduce(lambda crc, i: crc << 1 & 0xFFFF ^ (0x8F57
                      if (value << i ^ crc >> 8) & 0x80 else 0), range(bits), crc)

    def owen_crc16(self, packet):
        """ Вычисление контрольной суммы. """

        return reduce(lambda crc, val: self.fast_calc(val, crc, 8), packet, 0)

    def owen_hash(self, packet):
        """ Вычисление hash-функции. """

        return reduce(lambda crc, val: self.fast_calc(val << 1, crc, 7), packet, 0)

    @staticmethod
    def name2code(name):
        """ Преобразование локального идентификатора в числовой код. """

        owen_name = reduce(lambda x, ch: x[:-1] + [x[-1] + 1] if ch == "."
                           else x + [_OWEN_NAME[ch]], name.upper(), [])
        return owen_name + [_OWEN_NAME[" "]] * (4 - len(owen_name))

    @staticmethod
    def encode_frame(frame):
        """ Преобразование пакета из числового вида в строковый. """

        chars = (chr(71 + (num >> 4)) + chr(71 + (num & 0xF)) for num in frame)
        return ("#" + "".join(chars) + "\r").encode("ascii")

    @staticmethod
    def decode_frame(frame):
        """ Преобразование пакета из строкового вида в числовой. """

        return [(ord(i) - 71 << 4) + (ord(j) - 71 & 0xF)
                for i, j in zip(*[iter(frame[1:-1])] * 2)]

    @staticmethod
    def pack_value(frmt, value):
        """ Упаковка данных. """

        return None if value is None else list(bytearray(_OWEN_TYPE[frmt]["pack"](value)))

    @staticmethod
    def unpack_value(frmt, value, index):
        """ Распаковка данных. """

        if value:
            try:
                return _OWEN_TYPE[frmt]["unpack"](value, index)
            except error:
                errcode = _OWEN_TYPE["U8"]["unpack"](value, index)
                _logger.error("OwenProtocolError: error=%02X", errcode)

    def make_packet(self, flag, name, index, data=None):
        """ Формирование пакета для записи. """

        addr0, addr1 = (self.unit & 0xFF, 0) if self.addr_len_8 else \
                       (self.unit >> 3 & 0xFF, (self.unit & 0x07) << 5)
        if data is None:
            data = []
        if index is not None:
            data.extend([index >> 8 & 0xFF, index & 0xFF])

        cmd = self.owen_hash(self.name2code(name))
        frame = [addr0, addr1 | flag << 4 | len(data), cmd >> 8 & 0xFF, cmd & 0xFF] + data
        crc = self.owen_crc16(frame)
        packet = self.encode_frame(frame + [crc >> 8 & 0xFF, crc & 0xFF])

        _logger.debug("Send param: address=%d, flag=%d, size=%d, cmd=%04X, "
                      "data=%s, crc=%04X", self.unit, flag, len(data), cmd, data, crc)
        _logger.debug("Send frame: %r, size=%d", packet, len(packet))

        return packet

    def parse_response(self, packet, answer):
        """ Расшифровка прочитанного пакета. """

        _logger.debug("Recv frame: %r, size=%d", answer, len(answer))

        packet = packet.decode("ascii")
        answer = answer.decode("ascii")
        if not answer or answer[0] != "#" or answer[-1] != "\r":
            _logger.error("OwenProtocolError: Invalid message format")
            return None

        frame = self.decode_frame(answer)

        address = frame[0] if self.addr_len_8 else frame[0] << 3 | frame[1] >> 5
        flag = frame[1] >> 4 & 1
        size = frame[1] & 0xF
        cmd = frame[2] << 8 | frame[3]
        data = frame[4: 4 + size]
        crc = frame[-2] << 8 | frame[-1]

        _logger.debug("Recv param: address=%d, flag=%d, size=%d, cmd=%04X, "
                      "data=%s, crc=%04X", address, flag, size, cmd, data, crc)

        if self.owen_crc16(frame[:-2]) != crc:
            _logger.error("OwenProtocolError: Checksum error")
            return None
        if address != self.unit:
            _logger.error("OwenProtocolError: Sender and receiver addresses mismatch")
            return None
        if packet[7:9] != answer[7:9]:      # hash mismatch
            _logger.error("OwenProtocolError: error=%02X, hash=%02X%02X", *data)
            return None

        return answer == packet or bytearray(data)


__all__ = ["Owen"]
