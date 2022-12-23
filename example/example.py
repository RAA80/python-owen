#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep

from owen.transport import OwenSerialTransport, OwenModbusTransport
from owen.client import Client
from owen.device import TRM201

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    transport = OwenSerialTransport(port="COM5",
                                    baudrate=115200,
                                    stopbits=1,
                                    parity='N',
                                    bytesize=8,
                                    timeout=0.1)
    #transport.addr_len_8 = True    # длина адреса в битах: True=8, False=11

    #transport = OwenModbusTransport(method="rtu",
    #                                port="COM5",
    #                                baudrate=115200,
    #                                stopbits=2,
    #                                parity='N',
    #                                bytesize=8,        # "rtu": bytesize=8, "ascii": bytesize=7
    #                                timeout=0.1,
    #                                retry_on_empty=True)

    trm = Client(transport=transport, device=TRM201, unit=1)
    print(trm)

    ''' !!!
        Если параметр не использует индекс, т.е. index=None,
        либо прибор одноканальный и у параметра index=0,
        то индекс указывать необязательно

        Полная форма запроса:
        trm.getParam(name="A.LEn", index=None)
        trm.setParam(name="A.LEn", index=None, value=0)
    '''

    for key in TRM201['Owen']:
    #for key in TRM201['Modbus']:
        value = trm.getParam(name=key)
        print("{} = {}".format(key, value))
        sleep(0.1)

        if key in ("APLY", "INIT", "PRTL", "VER", "DEV", "N.ERR", "ATTR"):
            continue

        result = trm.setParam(name=key, value=value)
        print("{} = {}".format(key, result))
        sleep(0.1)
