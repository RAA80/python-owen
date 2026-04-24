#! /usr/bin/env python3

"""Функции для упаковки и распаковки разных типов данных протокола MODBUS."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypedDict

if TYPE_CHECKING:
    from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class TYPE(TypedDict):
    """Параметры типов для MODBUS_TYPE."""

    pack: Callable[[BinaryPayloadBuilder, int | float | str], None]
    unpack: Callable[[BinaryPayloadDecoder], int | float | str]
    size: int


MODBUS_TYPE: dict[str, TYPE] = {
    "U8": {
        "pack": lambda builder, value: builder.add_16bit_uint(int(value)),
        "unpack": lambda decoder: decoder.decode_16bit_uint(),
        "size": 1,
    },
    "I8": {
        "pack": lambda builder, value: builder.add_16bit_int(int(value)),
        "unpack": lambda decoder: decoder.decode_16bit_int(),
        "size": 1,
    },
    "U16": {
        "pack": lambda builder, value: builder.add_16bit_uint(int(value)),
        "unpack": lambda decoder: decoder.decode_16bit_uint(),
        "size": 1,
    },
    "I16": {
        "pack": lambda builder, value: builder.add_16bit_int(int(value)),
        "unpack": lambda decoder: decoder.decode_16bit_int(),
        "size": 1,
    },
    "U32": {
        "pack": lambda builder, value: builder.add_32bit_uint(int(value)),
        "unpack": lambda decoder: decoder.decode_32bit_uint(),
        "size": 2,
    },
    "I32": {
        "pack": lambda builder, value: builder.add_32bit_int(int(value)),
        "unpack": lambda decoder: decoder.decode_32bit_int(),
        "size": 2,
    },
    "F32": {
        "pack": lambda builder, value: builder.add_32bit_float(float(value)),
        "unpack": lambda decoder: decoder.decode_32bit_float(),
        "size": 2,
    },
    "STR6": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(6).decode("cp1251"),
        "size": 3,
    },
    "STR8": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(8).decode("cp1251"),
        "size": 4,
    },
    "STR16": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(16).decode("cp1251"),
        "size": 8,
    },
    "STR32": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(32).decode("cp1251"),
        "size": 16,
    },
    "STR64": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(64).decode("cp1251"),
        "size": 4,
    },
    "STR128": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(128).decode("cp1251"),
        "size": 8,
    },
    "STR256": {
        "pack": lambda builder, value: builder.add_string(str(value)),
        "unpack": lambda decoder: decoder.decode_string(256).decode("cp1251"),
        "size": 16,
    },
}
