#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from owen.client import OwenSerialClient, OwenModbusClient
from owen.protocol import Owen


class TRM(Owen):
    def __init__(self, client, unit):
        super(TRM, self).__init__(client, unit)

    def _get_ping_pong(self, packet):
        return {b'#GHHGTMOHHRTO\r': b'#GHGMTMOHJHJGJISSTGTIPLKK\r',         # чтение параметра "DEV" тип "STR"
                b'#GHHGHUTIKGJI\r': b'#GHGHHUTIGGJKGK\r',                   # чтение параметра "A.LEN" тип "U8" без индекса
                b'#GHHIRJURGGGGHQIV\r': b'#GHGJRJURGHGGGGQROU\r',           # чтение параметра "DP" тип "U8" с индексом
                b'#GHHGPVMIJIMK\r': b'#GHGIPVMIGGGHNHIR\r',                 # чтение параметра "ADDR" тип "U16" без индекса
                b'#GHHGROTVJNPQ\r': b'#GHGJROTVKIQJIOOJKN\r',               # чтение параметра "PV" тип "F24" без индекса
                b'#GHHIUSIGGGGGTJIT\r': b'#GHGLUSIGKKJROGGGGGPVUS\r',       # чтение параметра "SL.H" тип "F24" с индексом
                b'#GHHGGIJJRIQN\r': b'#GHGJGIJJKNRKMLLNJK\r',               # чтение параметра "N.ERR" тип "U24"

                b'#GHGHHUTIGGJKGK\r': b'#GHGHHUTIGGJKGK\r',                 # запись параметра "A.LEN" тип "U8" без индекса
                b'#GHGJQLQRGHGGGGPNOJ\r': b'#GHGJQLQRGHGGGGPNOJ\r',         # запись параметра "CMP" тип "U8" с индексом
                b'#GHGIPVMIGGGHNHIR\r': b'#GHGIPVMIGGGHNHIR\r',             # запись параметра "ADDR" тип "U16" без индекса
                b'#GHGJPPKMGGGGGGQMGJ\r': b'#GHGJPPKMGGGGGGQMGJ\r',         # запись параметра "R.OUT" тип "F24" без индекса
                b'#GHGLUSIGKKJROGGGGGPVUS\r': b'#GHGLUSIGKKJROGGGGGPVUS\r', # запись параметра "SL.H" тип "F24" с индексом
               }[packet]


class TestClient(unittest.TestCase):
    ''' This is the unittest for clients '''

    @patch("serial.Serial")
    def test_OwenSerialClient(self, mock_serial):
        transport = mock_serial
        device = {'Owen': {'A.LEN': {'type': 'U8', 'index': {None: None,}, 'min': 0, 'max': 1}}}
        unit = 1
        addr_len_8 = True

        client = OwenSerialClient(transport, device, unit, addr_len_8)
        client._owen = TRM(client=transport, unit=unit)

        # set correct params
        self.assertEqual(0, client.get_param(name="A.LEN", index=None))
        # set wrong index
        self.assertRaises(ValueError, lambda: client.get_param(name="A.LEN", index=2))
        # set correct params
        self.assertTrue(client.set_param(name="A.LEN", index=None, value=0))
        # set wrong index
        self.assertRaises(ValueError, lambda: client.set_param(name="A.LEN", index=2, value=0))
        # set wrong value
        self.assertRaises(ValueError, lambda: client.set_param(name="A.LEN", index=None, value=2))

    @patch("pymodbus.client.sync.ModbusSerialClient")
    def test_OwenModbusClient(self, mock_modbus):
        transport = mock_modbus
        device = {'Modbus': {'A.LEN': {'type': 'U16', 'index': {None: 0x0102,}, 'min': 0, 'max': 1, 'dp': None, 'precision': 0}}}
        unit = 1

        client = OwenModbusClient(transport, device, unit)

        self.assertTrue(client.connect())
        self.assertIsNone(client._error_check(name="A.LEN", retcode=None))
        self.assertTrue(client._error_check(name="A.LEN", retcode=1))
        # TODO: add get_param, set_param test


if __name__ == "__main__":
    unittest.main()
