#! /usr/bin/env python3

"""Функции для упаковки и распаковки разных типов данных."""

from binascii import hexlify, unhexlify
from decimal import Decimal
from struct import pack, unpack


def pack_str(value: str) -> bytes:
    """Упаковка данных типа STR."""

    return bytes(value[::-1], encoding="cp1251")


def unpack_str(value: bytes, index: int) -> str:
    """Распаковка данных типа STR."""

    return bytes(value[::-1]).decode("cp1251")


def pack_u24(value: tuple[int, int]) -> bytes:
    """Упаковка данных типа U24."""

    return pack(">BH", *value)[:3]


def unpack_u24(value: bytes, index: int) -> tuple[int, int]:
    """Распаковка данных типа U24."""

    return unpack(">BH", value[:3])


def pack_i8(value: int) -> bytes:
    """Упаковка данных типа I8."""

    return pack(">b", value)[:1]


def unpack_i8(value: bytes, index: int) -> int:
    """Распаковка данных типа I8."""

    return unpack(">b", value[:1])[0]


def pack_u8(value: int) -> bytes:
    """Упаковка данных типа U8."""

    return pack(">B", value)[:1]


def unpack_u8(value: bytes, index: int) -> int:
    """Распаковка данных типа U8."""

    return unpack(">B", value[:1])[0]


def pack_i16(value: int) -> bytes:
    """Упаковка данных типа I16."""

    return pack(">h", value)[:2]


def unpack_i16(value: bytes, index: int) -> int:
    """Распаковка данных типа I16."""

    return unpack(">h", value[:2])[0]


def pack_u16(value: int) -> bytes:
    """Упаковка данных типа U16."""

    return pack(">H", value)[:2]


def unpack_u16(value: bytes, index: int) -> int:
    """Распаковка данных типа U16."""

    return unpack(">H", value[:2])[0]


def pack_f24(value: float) -> bytes:
    """Упаковка данных типа F24."""

    return pack(">f", value)[:3]


def unpack_f24(value: bytes, index: int) -> float:
    """Распаковка данных типа F24."""

    return unpack(">f", value[:3] + b"\x00")[0]


def pack_f32(value: float) -> bytes:
    """Упаковка данных типа F32."""

    return pack(">f", value)[:4]


def unpack_f32(value: bytes, index: int) -> float:
    """Распаковка данных типа F32."""

    return unpack(">f", value[:4])[0]


def pack_f32t(value: tuple[float, int]) -> bytes:
    """Упаковка данных типа F32+T."""

    return pack(">fH", *value)[:6]


def unpack_f32t(value: bytes, index: int) -> tuple[float, int]:
    """Распаковка данных типа F32+T."""

    return unpack(">fH", value[:6])


def pack_i32(value: int) -> bytes:
    """Упаковка данных типа I32."""

    return pack(">i", value)[:4]


def unpack_i32(value: bytes, index: int) -> int:
    """Распаковка данных типа I32."""

    return unpack(">i", value[:4])[0]


def pack_u32(value: int) -> bytes:
    """Упаковка данных типа U32."""

    return pack(">I", value)[:4]


def unpack_u32(value: bytes, index: int) -> int:
    """Распаковка данных типа U32."""

    return unpack(">I", value[:4])[0]


def pack_sdot(value: float) -> bytes:
    """Упаковка данных типа STORED_DOT."""

    sign, digits, exponent = Decimal(str(value)).as_tuple()
    mantissa = int("".join(map(str, digits)))

    frmt, size, chunk = {mantissa < 16: (">B", 4, slice(1)),
                         mantissa >= 4096: (">I", 20, slice(1, 4)),
                        }.get(True, (">H", 12, slice(2)))

    bin_str = f"{sign:1b}{abs(exponent):03b}{mantissa:0{size}b}"
    return pack(frmt, int(bin_str, 2))[chunk]


def unpack_sdot(value: bytes, index: int) -> float:
    """Распаковка данных типа STORED_DOT."""

    value = bytearray(value)
    if index is not None:
        del value[-2:]

    arg, shift = {1: ((">B", value), 4),
                  2: ((">H", value), 12),
                  3: ((">I", b"\x00" + value), 20),
                 }[len(value)]

    data = unpack(*arg)[0]
    sign = data >> (shift + 3) & 1
    exponent = data >> shift & 7
    mantissa = data & (2 ** shift - 1)

    return (-1) ** sign * 10 ** (-exponent) * mantissa


def _encode_dot_u(value: float) -> bytes:
    """Упаковка данных типа DEC_DOTi."""

    value = int(value)
    length = len(str(value))
    length += length % 2
    hexstr = f"{value:0{length}d}"

    return unhexlify(hexstr)


def pack_dot0(value: float) -> bytes:
    """Упаковка данных типа DEC_DOT0."""

    return _encode_dot_u(value)


def unpack_dot0(value: bytes, index: int) -> int:
    """Распаковка данных типа DEC_DOT0."""

    value = bytearray(value)
    if index is not None:
        del value[-2:]

    return int(hexlify(value).decode())


def pack_dot3(value: float) -> bytes:
    """Упаковка данных типа DEC_DOT3."""

    return _encode_dot_u(value * 1000)


def unpack_dot3(value: bytes, index: int) -> float:
    """Распаковка данных типа DEC_DOT3."""

    value = bytearray(value)
    if index is not None:
        del value[-2:]

    return int(hexlify(value).decode()) / 1000.0


OWEN_TYPE = {"F32+T": {"pack": pack_f32t, "unpack": unpack_f32t},
             "SDOT":  {"pack": pack_sdot, "unpack": unpack_sdot},
             "DOT0":  {"pack": pack_dot0, "unpack": unpack_dot0},
             "DOT3":  {"pack": pack_dot3, "unpack": unpack_dot3},
             "F32":   {"pack": pack_f32,  "unpack": unpack_f32},
             "F24":   {"pack": pack_f24,  "unpack": unpack_f24},
             "U16":   {"pack": pack_u16,  "unpack": unpack_u16},
             "I16":   {"pack": pack_i16,  "unpack": unpack_i16},
             "U32":   {"pack": pack_u32,  "unpack": unpack_u32},
             "I32":   {"pack": pack_i32,  "unpack": unpack_i32},
             "U8":    {"pack": pack_u8,   "unpack": unpack_u8},
             "I8":    {"pack": pack_i8,   "unpack": unpack_i8},
             "U24":   {"pack": pack_u24,  "unpack": unpack_u24},   # для N.err
             "STR":   {"pack": pack_str,  "unpack": unpack_str}}
