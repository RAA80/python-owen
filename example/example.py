#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from pymodbus.client.sync import ModbusSerialClient
from serial import Serial

from owen.client import OwenModbusClient, OwenSerialClient
from owen.device import TRM201

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    transport = Serial(port="COM5",
                       baudrate=115200,
                       stopbits=1,
                       parity="N",
                       bytesize=8,
                       timeout=0.1)
    trm = OwenSerialClient(transport=transport, device=TRM201, unit=1, addr_len_8=True)     # длина адреса в битах: True=8, False=11

    # transport = ModbusSerialClient(method="rtu",
    #                                port="COM5",
    #                                baudrate=115200,
    #                                stopbits=2,
    #                                parity="N",
    #                                bytesize=8,        # "rtu": bytesize=8, "ascii": bytesize=7
    #                                timeout=0.1,
    #                                retry_on_empty=True)
    # trm = OwenModbusClient(transport=transport, device=TRM201, unit=1)

    print(trm)

    """ !!!
        Если параметр не использует индекс, т.е. index=None,
        либо прибор одноканальный и у параметра index=0,
        то индекс указывать необязательно

        Для многоканальных приборов (например ТРМ202) и протокола Modbus названия
        параметров (например IN.T1, IN.T2) для совместимости с протоколом ОВЕН
        преобразуются в:
        IN.T1 --> name="IN.T", index=0
        IN.T2 --> name="IN.T", index=1
    """

    name = "SP"     # Остальные названия параметров в файле 'device.py' для конкретного устройства
    value = trm.get_param(name=name, index=0)
    print("{} = {}".format(name, value))

    result = trm.set_param(name=name, index=0, value=value)
    print("{} = {}".format(name, result))
