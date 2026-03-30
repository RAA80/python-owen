#! /usr/bin/env python3

"""Реализация класса для работы по протоколу MODBUS."""

from __future__ import annotations

from operator import mul, truediv
from typing import TYPE_CHECKING, Callable

from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from owen.exception import OwenError
from owen.modbus.converter import MODBUS_TYPE

if TYPE_CHECKING:
    from pymodbus.pdu import ModbusPDU

    from owen.device._types import DEVICE, MODBUS


class Modbus:
    """Класс, описывающий протокол Modbus."""

    def __init__(self, unit: int, device: DEVICE, addr_len_8: bool) -> None:
        """Инициализация класса, описывающего протокол Modbus."""

        self.unit = unit
        self.device = device["modbus"]
        self.byteorder = device["byteorder"]
        self.wordorder = device["wordorder"]

    def read(self, address: int, count: int, unit: int) -> ModbusPDU:
        """Чтение данных."""

        raise NotImplementedError

    def write(self, address: int, builder: BinaryPayloadBuilder,
                    unit: int) -> ModbusPDU:
        """Запись данных."""

        raise NotImplementedError

    def check_index(self, name: str, index: int | None) -> tuple[MODBUS, int | None]:
        """Проверка индекса."""

        dev = self.device[name]

        if not index:
            index = None if None in dev["index"] else 0
        if index not in dev["index"]:
            msg = f"'{name}' does not support index '{index}'"
            raise OwenError(msg)

        return dev, index

    @staticmethod
    def check_error(retcode: ModbusPDU) -> bool:
        """Проверка возвращаемого значения на ошибку."""

        if retcode.isError():
            raise OwenError(retcode)
        return True

    def _read(self, dev: MODBUS, index: int | None) -> float | str:
        """Чтение данных из регистра Modbus."""

        count = {"U8": 1,  "STR8": 4,
                 "I8": 1,  "STR16": 8,
                 "I16": 1, "STR32": 16,
                 "U16": 1, "STR64": 4,
                 "I32": 2, "STR128": 8,
                 "U32": 2, "STR256": 16,
                 "F32": 2,
                }[dev["type"]]
        result = self.read(dev["index"][index], count, self.unit)
        self.check_error(result)
        decoder = BinaryPayloadDecoder.fromRegisters(registers=result.registers,
                                                     byteorder=self.byteorder,
                                                     wordorder=self.wordorder)
        return MODBUS_TYPE[dev["type"]]["unpack"](decoder)

    def modify_value(self, func: Callable[[float, float], float], dev: MODBUS,
                           index: int | None, value: float) -> float:
        """Преобразование значения к нужной точности."""

        if dev["dp"]:
            dp_dev = self.device[dev["dp"]]
            dp = self._read(dp_dev, index)
            value = func(value, 10.0**int(dp))

        prec = dev["precision"]
        return func(value, 10.0**prec) if prec else value

    def get_param(self, name: str, index: int | None = None) -> float | str:
        """Чтение данных из устройства."""

        dev, index = self.check_index(name, index)
        value = self._read(dev, index)
        return self.modify_value(truediv, dev, index, value)

    def set_param(self, name: str, index: int | None = None,
                        value: float | str | None = None) -> bool:
        """Запись данных в устройство."""

        dev, index = self.check_index(name, index)
        value = self.modify_value(mul, dev, index, value)

        builder = BinaryPayloadBuilder(payload=None,
                                       byteorder=self.byteorder,
                                       wordorder=self.wordorder)
        builder = MODBUS_TYPE[dev["type"]]["pack"](builder, value)

        result = self.write(dev["index"][index], builder, self.unit)
        return self.check_error(result)
