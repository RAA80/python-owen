#! /usr/bin/env python3

"""Пример использования библиотеки."""

import logging

from owen.client import (OwenDevice, ModbusSerialTransport,
                                     ModbusTcpTransport,
                                     OwenSerialTransport)
from owen.device import TRM202

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    transport = OwenSerialTransport(port="COM5",
                                    baudrate=115200,
                                    bytesize=8,
                                    parity="N",
                                    stopbits=1,
                                    timeout=1.0)
    # transport = ModbusSerialTransport(method="rtu",   # "rtu" / "ascii"
    #                                   port="COM5",
    #                                   baudrate=115200,
    #                                   bytesize=8,     # для "rtu": 8 / "ascii": 7
    #                                   parity="N",
    #                                   stopbits=2,
    #                                   timeout=1.0,
    #                                   retry_on_empty=True)
    # transport = ModbusTcpTransport(host="192.168.1.99", timeout=1.0)

    owen = OwenDevice(transport=transport, device=TRM202, unit=1, addr_len_8=True)

    """ !!!
        Для многоканальных приборов (например ТРМ202) и протокола Modbus названия
        параметров (например IN.T1, IN.T2) для совместимости с протоколом ОВЕН
        преобразуются в:
        IN.T1 --> name="IN.T", index=0
        IN.T2 --> name="IN.T", index=1
    """

    name = "SP"     # Остальные названия параметров в папке 'owen/device' для конкретного устройства
    value = owen.get_param(name=name, index=0)
    print(f"{name} = {value}")

    result = owen.set_param(name=name, index=0, value=value)
    print(f"{name} = {result}")
