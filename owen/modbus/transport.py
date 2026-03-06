#! /usr/bin/env python3
# mypy: disable-error-code="explicit-any"

"""Реализация классов транспорта для взаимодействия с устройством по
протоколу MODBUS.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pymodbus.client import ModbusSerialClient, ModbusTcpClient

if TYPE_CHECKING:
    from pymodbus.payload import BinaryPayloadBuilder
    from pymodbus.pdu import ModbusResponse


class ModbusSerialTransport:
    """Класс транспорта для взаимодействия с устройством по протоколу MODBUS
    через интерфейс RS485.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Инициализация класса транспорта для взаимодействия с устройством по
        протоколу MODBUS через интерфейс RS485.
        """

        self.socket = ModbusSerialClient(**kwargs)
        self.socket.connect()

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if hasattr(self, "socket"):
            self.socket.close()

    def write(self, address: int, builder: BinaryPayloadBuilder,
                    unit: int) -> ModbusResponse:
        """Запись данных по интерфейсу."""

        return self.socket.write_registers(address=address,
                                           values=builder.to_registers(),
                                           slave=unit)

    def read(self, address: int, count: int, unit: int) -> ModbusResponse:
        """Чтение данных по интерфейсу."""

        return self.socket.read_holding_registers(address=address,
                                                  count=count,
                                                  slave=unit)


class ModbusTcpTransport(ModbusSerialTransport):
    """Класс транспорта для взаимодействия с устройством по протоколу MODBUS TCP
    через интерфейс Ethernet.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Инициализация класса транспорта для взаимодействия с устройством по
        протоколу MODBUS TCP через интерфейс Ethernet.
        """

        self.socket = ModbusTcpClient(**kwargs)
        self.socket.connect()
