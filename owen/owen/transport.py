#! /usr/bin/env python3
# mypy: disable-error-code="explicit-any"

"""Реализация классов транспорта для взаимодействия с устройством по
протоколу ОВЕН.
"""

from __future__ import annotations

from typing import Any

from serial import Serial


class OwenSerialTransport:
    """Класс транспорта для взаимодействия с устройством по протоколу ОВЕН через
    интерфейс RS485.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Инициализация класса транспорта для взаимодействия с устройством по
        протоколу ОВЕН через интерфейс RS485.
        """

        self.socket = Serial(**kwargs)

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if hasattr(self, "socket"):
            self.socket.close()

    def write(self, packet: bytes) -> int | None:
        """Запись данных по интерфейсу."""

        self.socket.reset_input_buffer()
        self.socket.reset_output_buffer()

        return self.socket.write(packet)

    def read(self) -> bytes:
        """Чтение данных по интерфейсу."""

        return self.socket.read_until(b"\r")
