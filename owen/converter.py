#! /usr/bin/env python
# -*- coding: utf-8 -*-

from binascii import hexlify, unhexlify
from decimal import Decimal
from struct import pack, unpack


def pack_str(value):
    """ Упаковка данных типа STR. """

    return value[::-1]


def unpack_str(value, index):
    """ Распаковка данных типа STR. """

    return value[::-1]


def pack_u24(value):
    """ Упаковка данных типа U24. """

    return pack(">BH", value)[:3]


def unpack_u24(value, index):
    """ Распаковка данных типа U24. """

    return unpack(">BH", value[:3])


def pack_i8(value):
    """ Упаковка данных типа I8. """

    return pack(">b", value)[:1]


def unpack_i8(value, index):
    """ Распаковка данных типа I8. """

    return unpack(">b", value[:1])[0]


def pack_u8(value):
    """ Упаковка данных типа U8. """

    return pack(">B", value)[:1]


def unpack_u8(value, index):
    """ Распаковка данных типа U8. """

    return unpack(">B", value[:1])[0]


def pack_i16(value):
    """ Упаковка данных типа I16. """

    return pack(">h", value)[:2]


def unpack_i16(value, index):
    """ Распаковка данных типа I16. """

    return unpack(">h", value[:2])[0]


def pack_u16(value):
    """ Упаковка данных типа U16. """

    return pack(">H", value)[:2]


def unpack_u16(value, index):
    """ Распаковка данных типа U16. """

    return unpack(">H", value[:2])[0]


def pack_f24(value):
    """ Упаковка данных типа F24. """

    return pack(">f", value)[:3]


def unpack_f24(value, index):
    """ Распаковка данных типа F24. """

    return unpack(">f", value[:3] + b"\x00")[0]


def pack_f32(value):
    """ Упаковка данных типа F32. """

    return pack(">f", value)[:4]


def unpack_f32(value, index):
    """ Распаковка данных типа F32. """

    return unpack(">f", value[:4])[0]


def pack_f32t(value):
    """ Упаковка данных типа F32+T. """

    return pack(">fH", value)[:6]


def unpack_f32t(value, index):
    """ Распаковка данных типа F32+T. """

    return unpack(">fH", value[:6])


def pack_i32(value):
    """ Упаковка данных типа I32. """

    return pack(">i", value)[:4]


def unpack_i32(value, index):
    """ Распаковка данных типа I32. """

    return unpack(">i", value[:4])


def pack_u32(value):
    """ Упаковка данных типа U32. """

    return pack(">I", value)[:4]


def unpack_u32(value, index):
    """ Распаковка данных типа U32. """

    return unpack(">I", value[:4])


def pack_sdot(value):
    """ Упаковка данных типа STORED_DOT. """

    sign, mantissa, exponent = Decimal(str(value)).as_tuple()
    mantissa = int("".join(map(str, mantissa)))

    frmt, size, chunk = {mantissa < 16: (">B", 4, slice(1)),
                         mantissa >= 4096: (">I", 20, slice(1, 4)),
                        }.get(True, (">H", 12, slice(2)))

    bin_str = "{:1b}{:03b}{:0{}b}".format(sign, abs(exponent), mantissa, size)
    return pack(frmt, int(bin_str, 2))[chunk]


def unpack_sdot(value, index):
    """ Распаковка данных типа STORED_DOT. """

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


def _encode_dot_u(value):
    """ Упаковка данных типа DEC_DOTi. """

    length = len(str(int(value)))
    length = length + 1 if length % 2 else length
    hexstr = "{:0{}d}".format(value, length)

    return bytearray(unhexlify(hexstr))


def pack_dot0(value):
    """ Упаковка данных типа DEC_DOT0. """

    return _encode_dot_u(value)


def unpack_dot0(value, index):
    """ Распаковка данных типа DEC_DOT0. """

    if index is not None:
        del value[-2:]

    return int(hexlify(value).decode())


def pack_dot3(value):
    """ Упаковка данных типа DEC_DOT3. """

    return _encode_dot_u(value * 1000)


def unpack_dot3(value, index):
    """ Распаковка данных типа DEC_DOT3. """

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
