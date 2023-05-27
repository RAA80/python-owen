#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from owen.client import OwenSerialClient, OwenModbusClient


class FakeOwenSerialClient(OwenSerialClient):
    def __init__(self, transport, device, unit, addr_len_8):
        super(FakeOwenSerialClient, self).__init__(transport, device, unit, addr_len_8)

    def bus_exchange(self, packet):
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
        device = {'Owen': {'A.LEN': {'type': 'U8',  'index': {None: None,}, 'min': 0,     'max': 1},
                           'DEV':   {'type': 'STR', 'index': {None: None,}, 'min': "",    'max': ""},
                           'DP':    {'type': 'U8',  'index': {0: 0,},       'min': 0,     'max': 3},
                           'ADDR':  {'type': 'U16', 'index': {None: None,}, 'min': 0,     'max': 2047},
                           'PV':    {'type': 'F24', 'index': {None: None,}, 'min': -1999, 'max': 9999},
                           'SL.H':  {'type': 'F24', 'index': {0: 0,},       'min': -1999, 'max': 9999},
                           'N.ERR': {'type': 'U24', 'index': {None: None,}, 'min': 0,     'max': 255},
                           'CMP':   {'type': 'U8',  'index': {0: 0,},       'min': 0,     'max': 4},
                           'R.OUT': {'type': 'F24', 'index': {None: None,}, 'min': 0,     'max': 1},
                          }
                 }
        unit = 1
        addr_len_8 = True

        client = FakeOwenSerialClient(transport, device, unit, addr_len_8)

        # set correct params
        self.assertEqual(0, client.get_param(name="A.LEN", index=None))
        self.assertEqual(b'\xd2\xd0\xcc201', client.get_param(name="DEV", index=None))
        self.assertEqual(1, client.get_param(name="DP", index=0))
        self.assertEqual(1, client.get_param(name="ADDR", index=None))
        self.assertEqual(81.578125, client.get_param(name="PV", index=0))
        self.assertEqual(750.0, client.get_param(name="SL.H", index=0))
        self.assertEqual((71, 46181), client.get_param(name="N.ERR", index=None))
        # set wrong index
        self.assertRaises(ValueError, lambda: client.get_param(name="A.LEN", index=2))

        # set correct params
        self.assertTrue(client.set_param(name="A.LEN", index=None, value=0))
        self.assertTrue(client.set_param(name="CMP", index=0, value=1))
        self.assertTrue(client.set_param(name="ADDR", index=None, value=1))
        self.assertTrue(client.set_param(name="R.OUT", index=None, value=0.0))
        self.assertTrue(client.set_param(name="SL.H", index=0, value=750.0))
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
