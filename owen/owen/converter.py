#! /usr/bin/env python3

"""Функции для упаковки и распаковки разных типов данных протокола ОВЕН."""

from __future__ import annotations

from binascii import hexlify, unhexlify
from decimal import Decimal
from struct import pack, unpack


def pack_sdot(value: float) -> bytes:
    """Упаковка данных типа STORED_DOT."""

    sign, digits, exponent = Decimal(str(value)).as_tuple()
    mantissa = int(Decimal((0, digits, 0)))

    frmt, size, chunk = {mantissa < 16: (">B", 4, slice(1)),
                         mantissa >= 4096: (">I", 20, slice(1, 4)),
                        }.get(True, (">H", 12, slice(2)))

    bin_str = f"{sign:1b}{abs(exponent):03b}{mantissa:0{size}b}"
    return pack(frmt, int(bin_str, 2))[chunk]


def unpack_sdot(value: bytes) -> int | float:
    """Распаковка данных типа STORED_DOT."""

    data = int.from_bytes(value, "big")
    bin_str = f"{data:0{len(value) * 8}b}"

    sign = int(bin_str[0], 2)
    exponent = int(bin_str[1:4], 2)
    mantissa = int(bin_str[4:], 2)

    return (-1) ** sign * 10 ** (-exponent) * mantissa


def pack_dot0(value: float) -> bytes:
    """Упаковка данных типа DEC_DOT0."""

    s = str(int(value))
    return unhexlify(s.zfill(len(s) + len(s) % 2))


def unpack_dot0(value: bytes) -> int:
    """Распаковка данных типа DEC_DOT0."""

    return int(hexlify(value).decode())


OWEN_TYPE = {
    "U8": {
        "pack": lambda value: pack(">B", value)[:1],
        "unpack": lambda value: unpack(">B", value[:1])[0],
    },
    "I8": {
        "pack": lambda value: pack(">b", value)[:1],
        "unpack": lambda value: unpack(">b", value[:1])[0],
    },
    "U16": {
        "pack": lambda value: pack(">H", value)[:2],
        "unpack": lambda value: unpack(">H", value[:2])[0],
    },
    "I16": {
        "pack": lambda value: pack(">h", value)[:2],
        "unpack": lambda value: unpack(">h", value[:2])[0],
    },
    "U24": {
        "pack": lambda value: pack(">BH", *value)[:3],
        "unpack": lambda value: unpack(">BH", value[:3]),
    },
    "U32": {
        "pack": lambda value: pack(">I", value)[:4],
        "unpack": lambda value: unpack(">I", value[:4])[0],
    },
    "I32": {
        "pack": lambda value: pack(">i", value)[:4],
        "unpack": lambda value: unpack(">i", value[:4])[0],
    },
    "F24": {
        "pack": lambda value: pack(">f", value)[:3],
        "unpack": lambda value: unpack(">f", value[:3] + b"\x00")[0],
    },
    "F32": {
        "pack": lambda value: pack(">f", value)[:4],
        "unpack": lambda value: unpack(">f", value[:4])[0],
    },
    "F32+T": {
        "pack": lambda value: pack(">fH", *value)[:6],
        "unpack": lambda value: unpack(">fH", value[:6]),
    },
    "STR": {
        "pack": lambda value: str(value[::-1]).encode("cp1251"),
        "unpack": lambda value: bytes(value[::-1]).decode("cp1251"),
    },
    "SDOT": {
        "pack": pack_sdot,
        "unpack": unpack_sdot,
    },
    "DOT0": {
        "pack": pack_dot0,
        "unpack": unpack_dot0,
    },
    "DOT3": {
        "pack": lambda value: pack_dot0(value * 1000),
        "unpack": lambda value: unpack_dot0(value) / 1000.0,
    },
    "CLK": {
        "pack": lambda value: b"".join(pack_dot0(val).rjust(size, b"\x00")
                                       for val, size in zip(value, (3, 1, 1, 1))),
        "unpack": lambda value: tuple(unpack_dot0(value[slice(*chunk)])
                                      for chunk in ((0, 3), (3, 4), (4, 5), (5, 6))),
    },
}
