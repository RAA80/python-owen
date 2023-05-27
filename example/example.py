#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep
from serial import Serial
from pymodbus.client.sync import ModbusSerialClient

from owen.client import OwenSerialClient, OwenModbusClient
from owen.device import TRM201

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    transport = Serial(port="COM5",
                       baudrate=115200,
                       stopbits=1,
                       parity='N',
                       bytesize=8,
                       timeout=0.1)
    trm = OwenSerialClient(transport=transport, device=TRM201, unit=1, addr_len_8=True)     # длина адреса в битах: True=8, False=11

    #transport = ModbusSerialClient(method="rtu",
    #                               port="COM5",
    #                               baudrate=115200,
    #                               stopbits=2,
    #                               parity='N',
    #                               bytesize=8,        # "rtu": bytesize=8, "ascii": bytesize=7
    #                               timeout=0.1,
    #                               retry_on_empty=True)
    #trm = OwenModbusClient(transport=transport, device=TRM201, unit=1)

    print(trm)

    ''' !!!
        Все названия параметров ОВЕН должны быть в верхнем регистре
        Например: ADDR, A.LEN, BPS

        Полная форма запроса:
        get_param(name="ADDR", index=None)
        get_param(name="SP", index=0)
        set_param(name="ADDR", index=None, value=1)
        set_param(name="SP", index=0, value=20.0)

        Для многоканальных приборов (например ТРМ202) и протокола Modbus названия
        параметров (например IN.T1, IN.T2) для совместимости с протоколом ОВЕН
        преобразуются в:
        IN.T1 --> name="IN.T", index=0
        IN.T2 --> name="IN.T", index=1
    '''

    for key in TRM201['Owen']:
    #for key in TRM201['Modbus']:
        value = trm.get_param(name=key)
        print("{} = {}".format(key, value))
        sleep(0.1)

        if key in ("APLY", "INIT", "PRTL", "VER", "DEV", "N.ERR", "ATTR"):
            continue

        result = trm.set_param(name=key, value=value)
        print("{} = {}".format(key, result))
        sleep(0.1)
