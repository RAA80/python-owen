#! /usr/bin/env python3
# mypy: disable-error-code="explicit-any, assignment"

"""Реализация классов транспорта для взаимодействия с устройством по
протоколу MODBUS.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pymodbus.client import ModbusSerialClient, ModbusTcpClient

if TYPE_CHECKING:
    from pymodbus.pdu import ModbusPDU


class ModbusSerialTransport:
    """Класс транспорта для взаимодействия с устройством по протоколу MODBUS
    через интерфейс RS485.
    """

    def __init__(self, port: str,
                       baudrate: int = 9600,
                       bytesize: int = 8,
                       parity: str = "N",
                       stopbits: int = 2,
                       **kwargs: Any) -> None:
        """Инициализация класса транспорта для взаимодействия с устройством по
        протоколу MODBUS через интерфейс RS485.
        """

        self.socket = ModbusSerialClient(port=port,
                                         baudrate=baudrate,
                                         bytesize=bytesize,
                                         parity=parity,
                                         stopbits=stopbits,
                                         **kwargs)
        self.socket.connect()

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if hasattr(self, "socket"):
            self.socket.close()

    def write(self, address: int, payload: list[int], unit: int) -> ModbusPDU:
        """Запись данных по интерфейсу."""

        return self.socket.write_registers(address=address,
                                           values=payload,
                                           slave=unit)

    def read(self, address: int, count: int, unit: int) -> ModbusPDU:
        """Чтение данных по интерфейсу."""

        return self.socket.read_holding_registers(address=address,
                                                  count=count,
                                                  slave=unit)


class ModbusTcpTransport(ModbusSerialTransport):
    """Класс транспорта для взаимодействия с устройством по протоколу MODBUS TCP
    через интерфейс Ethernet.
    """

    def __init__(self, host: str, port: int = 502, **kwargs: Any) -> None:
        """Инициализация класса транспорта для взаимодействия с устройством по
        протоколу MODBUS TCP через интерфейс Ethernet.
        """

        self.socket = ModbusTcpClient(host=host, port=port, **kwargs)
        self.socket.connect()
