#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
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
    trm = OwenSerialClient(transport=transport, device=TRM201, unit=1)

    #transport = ModbusSerialClient(method="rtu",
    #                               port="COM5",
    #                               baudrate=115200,
    #                               stopbits=2,
    #                               parity='N',
    #                               bytesize=8,        # "rtu": bytesize=8, "ascii": bytesize=7
    #                               timeout=0.1,
    #                               retry_on_empty=True)
    #trm = OwenModbusClient(transport=transport, device=TRM201, unit=1)

    print (trm)

    ''' !!!
        Если параметр не использует индекс, т.е. index=None,
        либо прибор одноканальный и у параметра index=0,
        то индекс указывать необязательно
    '''

    #print ("STAT = {}".format(trm.getParam(name="STAT")))                  # for modbus only
    print ("A.LEn = {}".format(trm.getParam(name="A.LEn", index=None)))     # полная форма запроса
    print ("Addr = {}".format(trm.getParam(name="Addr")))
    print ("An.H = {}".format(trm.getParam(name="An.H")))
    print ("An.L = {}".format(trm.getParam(name="An.L")))
    print ("bPS = {}".format(trm.getParam(name="bPS")))
    print ("CmP = {}".format(trm.getParam(name="CmP")))
    print ("CtL = {}".format(trm.getParam(name="CtL")))
    print ("dAC = {}".format(trm.getParam(name="dAC")))
    print ("DEV = {}".format(trm.getParam(name="DEV")))
    print ("doF = {}".format(trm.getParam(name="doF")))
    print ("don = {}".format(trm.getParam(name="don")))
    print ("dP = {}".format(trm.getParam(name="dP")))
    print ("dPt = {}".format(trm.getParam(name="dPt")))
    print ("EdPt = {}".format(trm.getParam(name="EdPt")))
    print ("Fb = {}".format(trm.getParam(name="Fb")))
    print ("HYS = {}".format(trm.getParam(name="HYS")))
    print ("in.H = {}".format(trm.getParam(name="in.H")))
    print ("in.L = {}".format(trm.getParam(name="in.L")))
    print ("in.t = {}".format(trm.getParam(name="in.t")))
    print ("inF = {}".format(trm.getParam(name="inF")))
    print ("KU = {}".format(trm.getParam(name="KU")))
    print ("LEn = {}".format(trm.getParam(name="LEn")))
    print ("oAPt = {}".format(trm.getParam(name="oAPt")))
    print ("oEr = {}".format(trm.getParam(name="oEr")))
    print ("PROT = {}".format(trm.getParam(name="PROT")))
    print ("PrtY = {}".format(trm.getParam(name="PrtY")))
    print ("PV = {}".format(trm.getParam(name="PV")))
    print ("r-L = {}".format(trm.getParam(name="r-L")))
    print ("r.oUt = {}".format(trm.getParam(name="r.oUt")))
    print ("rESt = {}".format(trm.getParam(name="rESt")))
    print ("rSdL = {}".format(trm.getParam(name="rSdL")))
    print ("Sbit = {}".format(trm.getParam(name="Sbit")))
    print ("SH = {}".format(trm.getParam(name="SH")))
    print ("SL.H = {}".format(trm.getParam(name="SL.H")))
    print ("SL.L = {}".format(trm.getParam(name="SL.L")))
    print ("SP = {}".format(trm.getParam(name="SP")))
    print ("Sqr = {}".format(trm.getParam(name="Sqr")))
    print ("toF = {}".format(trm.getParam(name="toF")))
    print ("ton = {}".format(trm.getParam(name="ton")))
    print ("VER = {}".format(trm.getParam(name="VER")))
    print ("wtPt = {}".format(trm.getParam(name="wtPt")))
    print ("XP = {}".format(trm.getParam(name="XP")))

    print ("")

    print ("A.LEn = {}".format(trm.setParam(name="A.LEn", index=None, value=0)))    # полная форма запроса
    print ("Addr = {}".format(trm.setParam(name="Addr", value=1)))
    print ("An.H = {}".format(trm.setParam(name="An.H", value=1300.0)))     # for modbus depend from DP
    print ("An.L = {}".format(trm.setParam(name="An.L", value=-199.9)))     # for modbus depend from DP
    #print ("APLY = {}".format(trm.setParam(name="APLY")))                  # for modbus value=1
    print ("bPS = {}".format(trm.setParam(name="bPS", value=8)))
    print ("CmP = {}".format(trm.setParam(name="CmP", value=1)))
    print ("CtL = {}".format(trm.setParam(name="CtL", value=0)))
    print ("dAC = {}".format(trm.setParam(name="dAC", value=0)))
    print ("doF = {}".format(trm.setParam(name="doF", value=0)))
    print ("don = {}".format(trm.setParam(name="don", value=0)))
    print ("dP = {}".format(trm.setParam(name="dP", value=1)))
    print ("dPt = {}".format(trm.setParam(name="dPt", value=1)))
    print ("EdPt = {}".format(trm.setParam(name="EdPt", value=0)))
    print ("Fb = {}".format(trm.setParam(name="Fb", value=0.0)))            # for modbus depend from DP
    print ("HYS = {}".format(trm.setParam(name="HYS", value=1.0)))          # for modbus depend from DP
    print ("inF = {}".format(trm.setParam(name="inF", value=0.0)))          # for modbus depend from DP
    print ("in.H = {}".format(trm.setParam(name="in.H", value=1300.0)))     # for modbus depend from DP
    print ("in.L = {}".format(trm.setParam(name="in.L", value=-199.9)))     # for modbus depend from DP
    print ("in.t = {}".format(trm.setParam(name="in.t", value=16)))
    #print ("INIT = {}".format(trm.setParam(name="INIT")))                  # for modbus value=1
    print ("KU = {}".format(trm.setParam(name="KU", value=1.0)))            # for modbus value*=1000
    print ("LEn = {}".format(trm.setParam(name="LEn", value=1)))
    print ("oAPt = {}".format(trm.setParam(name="oAPt", value=0)))
    print ("oEr = {}".format(trm.setParam(name="oEr", value=0)))
    print ("PROT = {}".format(trm.setParam(name="PROT", value=0)))
    #print ("PRTL = {}".format(trm.setParam(name="PRTL")))                  # for modbus value=1
    print ("PrtY = {}".format(trm.setParam(name="PrtY", value=0)))
    print ("r-L = {}".format(trm.setParam(name="r-L", value=0)))
    print ("r.oUt = {}".format(trm.setParam(name="r.oUt", value=0.0)))      # for modbus value*=1000
    print ("rESt = {}".format(trm.setParam(name="rESt", value=100)))
    print ("rSdL = {}".format(trm.setParam(name="rSdL", value=20)))
    print ("Sbit = {}".format(trm.setParam(name="Sbit", value=0)))
    print ("SH = {}".format(trm.setParam(name="SH", value=0.0)))            # for modbus depend from DP
    print ("SL.H = {}".format(trm.setParam(name="SL.H", value=1300.0)))     # for modbus depend from DP
    print ("SL.L = {}".format(trm.setParam(name="SL.L", value=-199.9)))     # for modbus depend from DP
    print ("SP = {}".format(trm.setParam(name="SP", value=25)))             # for modbus depend from DP
    print ("Sqr = {}".format(trm.setParam(name="Sqr", value=1)))
    print ("toF = {}".format(trm.setParam(name="toF", value=0)))
    print ("ton = {}".format(trm.setParam(name="ton", value=0)))
    print ("wtPt = {}".format(trm.setParam(name="wtPt", value=0)))
    print ("XP = {}".format(trm.setParam(name="XP", value=1.0)))            # for modbus depend from DP

    print ("")

    print ("N.err = {}".format(trm.getParam(name="N.err")))
