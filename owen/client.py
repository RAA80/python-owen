#! /usr/bin/env python3

"""Реализация класса клиента."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from owen.modbus.protocol import Modbus
from owen.modbus.transport import ModbusSerialTransport, ModbusTcpTransport
from owen.owen.protocol import Owen
from owen.owen.transport import OwenSerialTransport

if TYPE_CHECKING:
    from owen.device._types import DEVICE

Transport = Union[ModbusSerialTransport, ModbusTcpTransport, OwenSerialTransport]


class OwenDevice:
    """Класс клиента для работы с устройствами ОВЕН."""

    def __init__(self, transport: Transport, device: DEVICE, unit: int,
                       addr_len_8: bool = True) -> None:
        """Инициализация класса клиента для работы с устройствами ОВЕН.

        Args:
            transport: Тип используемого транспорта
            device: Название устройства (например: TRM201)
            unit: Адрес устройства (0...2047 - для Овен, 0...255 - для Modbus)
            addr_len_8: Длина адреса в битах (True=8, False=11). Для Modbus игнорируется

        """

        self._transport = transport
        self._protocol = {OwenSerialTransport: Owen,
                          ModbusSerialTransport: Modbus,
                          ModbusTcpTransport: Modbus,
                         }[transport.__class__](unit, device, addr_len_8)
        self._protocol.read = transport.read
        self._protocol.write = transport.write

    def get_param(self, name: str, index: int | None = None) -> float | str:
        """Чтение значения параметра устройства."""

        return self._protocol.get_param(name.upper(), index)

    def set_param(self, name: str, index: int | None = None,
                        value: float | str | None = None) -> bool:
        """Запись нового значения параметра устройства."""

        return self._protocol.set_param(name.upper(), index, value)


__all__ = ["ModbusSerialTransport", "ModbusTcpTransport",
           "OwenDevice", "OwenSerialTransport"]
