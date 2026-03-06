#! /usr/bin/env python3

"""Функции для упаковки и распаковки разных типов данных протокола MODBUS."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


def pack_str(builder: BinaryPayloadBuilder, value: str) -> BinaryPayloadBuilder:
    """Упаковка данных типа STR."""

    builder.add_string(str(value))
    return builder


def unpack_str8(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR8."""

    return decoder.decode_string(8)


def unpack_str16(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR16."""

    return decoder.decode_string(16)


def unpack_str32(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR32."""

    return decoder.decode_string(32)


def unpack_str64(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR64."""

    return decoder.decode_string(64)


def unpack_str128(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR128."""

    return decoder.decode_string(128)


def unpack_str256(decoder: BinaryPayloadDecoder) -> str:
    """Распаковка данных типа STR256."""

    return decoder.decode_string(256)


def pack_i8(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа I8."""

    builder.add_16bit_int(int(value))
    return builder


def unpack_i8(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа I8."""

    return decoder.decode_16bit_int()


def pack_u8(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа U8."""

    builder.add_16bit_uint(int(value))
    return builder


def unpack_u8(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа U8."""

    return decoder.decode_16bit_uint()


def pack_i16(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа I16."""

    builder.add_16bit_int(int(value))
    return builder


def unpack_i16(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа I16."""

    return decoder.decode_16bit_int()


def pack_u16(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа U16."""

    builder.add_16bit_uint(int(value))
    return builder


def unpack_u16(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа U16."""

    return decoder.decode_16bit_uint()


def pack_f32(builder: BinaryPayloadBuilder, value: float) -> BinaryPayloadBuilder:
    """Упаковка данных типа F32."""

    builder.add_32bit_float(float(value))
    return builder


def unpack_f32(decoder: BinaryPayloadDecoder) -> float:
    """Распаковка данных типа F32."""

    return decoder.decode_32bit_float()


def pack_i32(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа I32."""

    builder.add_32bit_int(int(value))
    return builder


def unpack_i32(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа I32."""

    return decoder.decode_32bit_int()


def pack_u32(builder: BinaryPayloadBuilder, value: int) -> BinaryPayloadBuilder:
    """Упаковка данных типа U32."""

    builder.add_32bit_uint(int(value))
    return builder


def unpack_u32(decoder: BinaryPayloadDecoder) -> int:
    """Распаковка данных типа U32."""

    return decoder.decode_32bit_uint()


MODBUS_TYPE = {"F32":    {"pack": pack_f32, "unpack": unpack_f32},
               "U16":    {"pack": pack_u16, "unpack": unpack_u16},
               "I16":    {"pack": pack_i16, "unpack": unpack_i16},
               "U32":    {"pack": pack_u32, "unpack": unpack_u32},
               "I32":    {"pack": pack_i32, "unpack": unpack_i32},
               "U8":     {"pack": pack_u8,  "unpack": unpack_u8},
               "I8":     {"pack": pack_i8,  "unpack": unpack_i8},
               "STR8":   {"pack": pack_str, "unpack": unpack_str8},
               "STR16":  {"pack": pack_str, "unpack": unpack_str16},
               "STR32":  {"pack": pack_str, "unpack": unpack_str32},
               "STR64":  {"pack": pack_str, "unpack": unpack_str64},
               "STR128": {"pack": pack_str, "unpack": unpack_str128},
               "STR256": {"pack": pack_str, "unpack": unpack_str256},
              }
