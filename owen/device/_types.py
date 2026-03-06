#! /usr/bin/env python3

from __future__ import annotations

from typing import TypedDict

# Назначение полей таблиц настроек:
#   1. Тип протокола Owen
#       * Название параметра (в верхнем регистре)
#           - Тип параметра
#           - Словарь индексов (None - индекса нет; 0,1 и т.д) + адрес индекса
#   2. Тип протокола Modbus
#       * Название параметра (в верхнем регистре)
#           - Тип параметра
#           - Словарь индексов (None - индекса нет; 0,1 и т.д) + адрес Modbus
#           - Признак зависимости от другого параметра: название параметра или None
#           - Кол-во знаков после запятой
#   3. Порядок байт в протоколе Modbus: ">", "<"
#   4. Порядок регистров в протоколе Modbus: ">", "<"

# Поддерживаемые типы данных:
#   I8, U8 - signed and unsigned char (1 byte)
#   I16, U16 - signed and unsigned short (2 bytes)
#   I32, U32 - signed and unsigned int (4 bytes)
#   U24 - for N.ERR (3 bytes)
#   F24, F32 - float (3 or 4 bytes)
#   F32+T - float + time modificator (6 bytes)
#   STRxx - string (xx bytes)
#   SDOT - STORED_DOT
#   DOT0, DOT3 - DEC_DOT0, DEC_DOT3
#   CLK - CLK_FRM


class OWEN(TypedDict):
    """Параметры типов протокола ОВЕН."""

    type: str
    index: dict[int | None, int | None]


class MODBUS(TypedDict):
    """Параметры типов протокола MODBUS."""

    type: str
    index: dict[int | None, int]
    dp: str | None
    precision: int


class DEVICE(TypedDict, total=False):
    """Параметры типов устройств ОВЕН."""

    owen: dict[str, OWEN]
    modbus: dict[str, MODBUS]
    byteorder: str
    wordorder: str
