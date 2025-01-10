#! /usr/bin/env python3

"""Реализация протокола взаимодействия ОВЕН."""

from __future__ import annotations

import logging
from functools import reduce
from struct import error, unpack

from .converter import OWEN_TYPE

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


HEADER = ord("#")
FOOTER = ord("\r")
OWEN_ASCII = {"0":  0, "1":  2, "2":  4, "3":  6, "4":  8,
              "5": 10, "6": 12, "7": 14, "8": 16, "9": 18,
              "A": 20, "B": 22, "C": 24, "D": 26, "E": 28,
              "F": 30, "G": 32, "H": 34, "I": 36, "J": 38,
              "K": 40, "L": 42, "M": 44, "N": 46, "O": 48,
              "P": 50, "Q": 52, "R": 54, "S": 56, "T": 58,
              "U": 60, "V": 62, "W": 64, "X": 66, "Y": 68,
              "Z": 70, "-": 72, "_": 74, "/": 76, " ": 78}


class OwenError(Exception):
    pass


class Owen:
    """Класс, описывающий протокол ОВЕН."""

    def __init__(self, unit: int, addr_len_8: bool) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self.unit = unit
        self.addr_len_8 = addr_len_8

    @staticmethod
    def fast_calc(value: int, crc: int, bits: int) -> int:
        """Вычисление значения полинома."""

        return reduce(lambda crc, i: crc << 1 & 0xFFFF ^ (0x8F57
                      if (value << i ^ crc >> 8) & 0x80 else 0), range(bits), crc)

    def owen_crc16(self, packet: tuple[int, ...]) -> int:
        """Вычисление контрольной суммы."""

        return reduce(lambda crc, val: self.fast_calc(val, crc, 8), packet, 0)

    def owen_hash(self, packet: tuple[int, ...]) -> int:
        """Вычисление hash-функции."""

        return reduce(lambda crc, val: self.fast_calc(val << 1, crc, 7), packet, 0)

    @staticmethod
    def name2code(name: str) -> tuple[int, ...]:
        """Преобразование локального идентификатора в числовой код."""

        code: list[int] = reduce(lambda x, ch: [*x[:-1], x[-1] + 1] if ch == "."
                                 else [*x, OWEN_ASCII[ch]], name.upper(), [])
        return (*code, *[OWEN_ASCII[" "]] * (4 - len(code)))

    @staticmethod
    def encode_frame(frame: tuple[int, ...]) -> bytes:
        """Преобразование пакета из числового вида в строковый."""

        chars = ([71 + (num >> 4), 71 + (num & 0xF)] for num in frame)
        return bytes([HEADER, *sum(chars, []), FOOTER])

    @staticmethod
    def decode_frame(frame: bytes) -> tuple[int, ...]:
        """Преобразование пакета из строкового вида в числовой."""

        pairs = zip(*[iter(frame[1:-1])] * 2)
        return tuple((i - 71 << 4) + (j - 71 & 0xF) for i, j in pairs)

    @staticmethod
    def pack_value(frmt: str, value: float | str | None) -> tuple[int, ...] | None:
        """Упаковка данных заданного формата."""

        return None if value is None else tuple(OWEN_TYPE[frmt]["pack"](value))

    @staticmethod
    def unpack_value(frmt: str, value: bytes, index: int | None) -> float | str:
        """Распаковка данных заданного формата."""

        try:
            return OWEN_TYPE[frmt]["unpack"](value, index)
        except error:
            errcode = OWEN_TYPE["U8"]["unpack"](value, index)
            msg = f"errorcode = {errcode:02X}"
            raise OwenError(msg) from None

    def make_packet(self, flag: int, name: str, index: int | None,
                          data: tuple[int, ...] | None = None) -> bytes:
        """Формирование пакета для записи."""

        addr0, addr1 = (self.unit & 0xFF, 0) if self.addr_len_8 else \
                       (self.unit >> 3 & 0xFF, (self.unit & 0x07) << 5)
        data = data or ()
        if index is not None:
            data = (*data, *index.to_bytes(2, "big"))

        cmd = self.owen_hash(self.name2code(name))
        frame = (addr0, addr1 | flag << 4 | len(data), *cmd.to_bytes(2, "big"), *data)
        crc = self.owen_crc16(frame)
        packet = self.encode_frame((*frame, *crc.to_bytes(2, "big")))

        _logger.debug("Send param: address=%d, flag=%d, size=%d, cmd=%04X, "
                      "index=%s, data=%s, crc=%04X", self.unit, flag, len(data),
                      cmd, index, data, crc)
        _logger.debug("Send frame: %r, size=%d", packet, len(packet))

        return packet

    def parse_response(self, packet: bytes, answer: bytes) -> bytes:
        """Расшифровка прочитанного пакета."""

        _logger.debug("Recv frame: %r, size=%d", answer, len(answer))

        if not answer or answer[0] != HEADER or answer[-1] != FOOTER:
            msg = "Invalid message format"
            raise OwenError(msg)

        frame = self.decode_frame(answer)

        address = frame[0] if self.addr_len_8 else frame[0] << 3 | frame[1] >> 5
        flag = frame[1] >> 4 & 1
        size = frame[1] & 0xF
        cmd, *data, crc = unpack(f">H{size}BH", bytes(frame[2:]))

        _logger.debug("Recv param: address=%d, flag=%d, size=%d, cmd=%04X, data=%s, "
                      "crc=%04X", address, flag, size, cmd, tuple(data), crc)

        if self.owen_crc16(frame[:-2]) != crc:
            msg = "Checksum error"
            raise OwenError(msg)
        if address != self.unit:
            msg = "Sender and receiver addresses mismatch"
            raise OwenError(msg)
        if packet[7:9] != answer[7:9]:      # hash mismatch
            msg = "Network error={:02X}, hash={:02X}{:02X}".format(*data)
            raise OwenError(msg)

        return bytes(data)


__all__ = ["Owen"]
