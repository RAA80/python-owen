#! /usr/bin/env python3

"""Реализация класса клиента для управления контроллером ОВЕН."""

from __future__ import annotations

from operator import mul, truediv
from typing import TYPE_CHECKING, Callable

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from .protocol import Owen, OwenError

if TYPE_CHECKING:
    from pymodbus.client.sync import ModbusSerialClient
    from pymodbus.pdu import ModbusResponse
    from serial import Serial

    from .device import MODBUS_PARAMS, OWEN_DEVICE, OWEN_PARAMS


class ClientMixin:
    """Класс-примесь клиента."""

    @staticmethod
    def check_index(name: str, dev: OWEN_PARAMS | MODBUS_PARAMS,
                    index: int | None) -> int | None:
        """Проверка индекса."""

        if not index:
            index = None if None in dev["index"] else 0
        if index not in dev["index"]:
            msg = f"'{name}' does not support index '{index}'"
            raise OwenError(msg)

        return index

    @staticmethod
    def check_value(name: str, dev: OWEN_PARAMS | MODBUS_PARAMS,
                    value: float | str | None) -> None:
        """Проверка данных."""

        if all([value is None, dev["min"] is not None, dev["max"] is not None]) or \
           all([value is not None, dev["min"] == dev["max"] is None or
                                   value < dev["min"] or value > dev["max"]]):  # type: ignore
            msg = f"An '{name}' value of '{value}' is out of range"
            raise OwenError(msg)


class OwenSerialClient(ClientMixin):
    """Класс клиента для взаимодействия с устройством по протоколу ОВЕН."""

    def __init__(self, transport: Serial, device: OWEN_DEVICE, unit: int, *,
                       addr_len_8: bool = True) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self.socket = transport
        self.unit = unit
        self.device = device
        self.addr_len_8 = addr_len_8

        self._owen = Owen(self.unit, addr_len_8)

    def __repr__(self) -> str:
        """Строковое представление объекта."""

        return (f"{type(self).__name__}(transport={self.socket}, unit={self.unit}, "
                f"addr_len_8={self.addr_len_8})")

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if self.socket:
            self.socket.close()

    def bus_exchange(self, packet: bytes) -> bytes:
        """Обмен по интерфейсу."""

        self.socket.reset_input_buffer()
        self.socket.reset_output_buffer()

        self.socket.write(packet)
        return self.socket.read_until(b"\r")

    def send_message(self, flag: int, name: str, index: int | None,
                           data: tuple[int, ...] | None = None) -> bytes:
        """Подготовка данных для обмена."""

        packet = self._owen.make_packet(flag, name, index, data)
        answer = self.bus_exchange(packet)
        return self._owen.parse_response(packet, answer)

    def get_param(self, name: str, index: int | None = None) -> float | str:
        """Чтение данных из устройства."""

        dev = self.device["Owen"][name.upper()]
        index = self.check_index(name, dev, index)
        result = self.send_message(1, name, index)
        return self._owen.unpack_value(dev["type"], result, index)

    def set_param(self, name: str, index: int | None = None,
                        value: float | str | None = None) -> bool:
        """Запись данных в устройство."""

        dev = self.device["Owen"][name.upper()]
        index = self.check_index(name, dev, index)
        self.check_value(name, dev, value)
        data = self._owen.pack_value(dev["type"], value)
        return bool(self.send_message(0, name, index, data))


class OwenModbusClient(ClientMixin):
    """Класс клиента для взаимодействия с устройством по протоколу Modbus."""

    def __init__(self, transport: ModbusSerialClient, device: OWEN_DEVICE,
                       unit: int) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self.socket = transport
        self.unit = unit
        self.device = device

        self.socket.connect()

    def __repr__(self) -> str:
        """Строковое представление объекта."""

        return f"{type(self).__name__}(transport={self.socket}, unit={self.unit})"

    def __del__(self) -> None:
        """Закрытие соединения с устройством при удалении объекта."""

        if self.socket:
            self.socket.close()

    @staticmethod
    def check_error(retcode: ModbusResponse) -> bool:
        """Проверка возвращаемого значения на ошибку."""

        if retcode.isError():
            raise OwenError(retcode)
        return True

    def _read(self, dev: MODBUS_PARAMS, index: int | None) -> float | str:
        """Чтение данных из регистра Modbus."""

        count = {"U16": 1, "I16": 1, "U32": 2, "I32": 2, "F32": 2, "STR": 4,
                }[dev["type"]]
        result = self.socket.read_holding_registers(address=dev["index"][index],
                                                    count=count,
                                                    unit=self.unit)
        self.check_error(result)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big)

        return {"U16": decoder.decode_16bit_uint,
                "I16": decoder.decode_16bit_int,
                "U32": decoder.decode_32bit_uint,
                "I32": decoder.decode_32bit_int,
                "F32": decoder.decode_32bit_float,
                "STR": lambda: decoder.decode_string(8),
                }[dev["type"]]()

    def modify_value(self, func: Callable[[float, float], float], dev: MODBUS_PARAMS,
                           index: int | None, value: float) -> float:
        """Преобразование значения к нужной точности."""

        if dev["dp"]:
            dp_dev = self.device["Modbus"][dev["dp"]]
            dp = self._read(dp_dev, index)
            value = func(value, 10.0**int(dp))

        prec = dev["precision"]
        return func(value, 10.0**prec) if prec else value

    def get_param(self, name: str, index: int | None = None) -> float | str:
        """Чтение данных из устройства."""

        dev = self.device["Modbus"][name.upper()]
        index = self.check_index(name, dev, index)
        value = self._read(dev, index)
        return self.modify_value(truediv, dev, index, value)

    def set_param(self, name: str, index: int | None = None,
                        value: float | str | None = None) -> bool:
        """Запись данных в устройство."""

        dev = self.device["Modbus"][name.upper()]
        index = self.check_index(name, dev, index)
        self.check_value(name, dev, value)
        value = self.modify_value(mul, dev, index, value)

        builder = BinaryPayloadBuilder(None, Endian.Big)
        {"U16": lambda value: builder.add_16bit_uint(int(value)),
         "I16": lambda value: builder.add_16bit_int(int(value)),
         "U32": lambda value: builder.add_32bit_uint(int(value)),
         "I32": lambda value: builder.add_32bit_int(int(value)),
         "F32": lambda value: builder.add_32bit_float(float(value)),
         "STR": lambda value: builder.add_string(str(value)),
        }[dev["type"]](value)

        result = self.socket.write_registers(address=dev["index"][index],
                                             values=builder.build(),
                                             skip_encode=True,
                                             unit=self.unit)
        return self.check_error(result)


__all__ = ["OwenModbusClient", "OwenSerialClient"]
