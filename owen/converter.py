#! /usr/bin/env python
# -*- coding: utf-8 -*-

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


def pack_sdot(value):
    """ Упаковка данных типа SDOT. """

    sign = int(value < 0)
    exponent = len(str(value).split(".")[1])
    mantissa = int(str(abs(value)).replace(".", ""))

    if mantissa < 16:
        result = int("{:1b}{:03b}{:04b}".format(sign, exponent, mantissa), 2)
        return pack(">B", result)[:1]

    elif 16 <= mantissa < 4096:
        result = int("{:1b}{:03b}{:012b}".format(sign, exponent, mantissa), 2)
        return pack(">H", result)[:2]

    elif mantissa >= 4096:
        result = int("{:1b}{:03b}{:020b}".format(sign, exponent, mantissa), 2)
        return pack(">I", result)[1:4]


def unpack_sdot(value, index):
    """ Распаковка данных типа SDOT. """

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
