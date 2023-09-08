#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from owen.client import OwenSerialClient, OwenModbusClient


test_device = {'Owen': {'A.LEN': {'type': 'U8',  'index': {None: None}, 'min': 0,     'max': 1},
                        'DEV':   {'type': 'STR', 'index': {None: None}, 'min': "",    'max': ""},
                        'DP':    {'type': 'U8',  'index': {0: 0},       'min': 0,     'max': 3},
                        'ADDR':  {'type': 'U16', 'index': {None: None}, 'min': 0,     'max': 2047},
                        'PV':    {'type': 'F24', 'index': {None: None}, 'min': -1999, 'max': 9999},
                        'SL.H':  {'type': 'F24', 'index': {0: 0},       'min': -1999, 'max': 9999},
                        'N.ERR': {'type': 'U24', 'index': {None: None}, 'min': 0,     'max': 255},
                        'CMP':   {'type': 'U8',  'index': {0: 0},       'min': 0,     'max': 4},
                        'R.OUT': {'type': 'F24', 'index': {None: None}, 'min': 0,     'max': 1},
                        'INIT':  {'type': 'U8',  'index': {None: None}, 'min': None,  'max': None},
                       },
               'Modbus': {'A.LEN': {'type': 'U16', 'index': {None: 0x0102}, 'min': 0, 'max': 1, 'dp': None, 'precision': 0}}
              }


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
                b'#GHGGGGUPJSUL\r': b'',                                    # запись параметра "INIT" тип "U8" без индексом
               }[packet]


class TestOwenSerialClient(unittest.TestCase):
    @patch("serial.Serial")
    def setUp(self, mock_serial):
        self.client = FakeOwenSerialClient(transport=mock_serial,
                                           device=test_device,
                                           unit=1,
                                           addr_len_8=True)

    def test_connect(self):
        self.assertTrue(self.client.connect())

    def test_get_param(self):
        # correct index
        self.assertEqual(0, self.client.get_param(name="A.LEN", index=None))
        self.assertEqual(b'\xd2\xd0\xcc201', self.client.get_param(name="DEV", index=None))
        self.assertEqual(1, self.client.get_param(name="DP", index=0))
        self.assertEqual(1, self.client.get_param(name="ADDR", index=None))
        self.assertEqual(81.578125, self.client.get_param(name="PV", index=0))
        self.assertEqual(750.0, self.client.get_param(name="SL.H", index=0))
        self.assertEqual((71, 46181), self.client.get_param(name="N.ERR", index=None))
        # wrong index
        self.assertRaises(ValueError, lambda: self.client.get_param(name="A.LEN", index=2))

    def test_set_param(self):
        # correct index and value
        self.assertTrue(self.client.set_param(name="A.LEN", index=None, value=0))
        self.assertTrue(self.client.set_param(name="CMP", index=0, value=1))
        self.assertTrue(self.client.set_param(name="ADDR", index=None, value=1))
        self.assertTrue(self.client.set_param(name="R.OUT", index=None, value=0.0))
        self.assertTrue(self.client.set_param(name="SL.H", index=0, value=750.0))
        self.assertIsNone(self.client.set_param(name="INIT", index=None, value=None))
        # wrong index
        self.assertRaises(ValueError, lambda: self.client.set_param(name="A.LEN", index=2, value=0))
        # wrong value
        self.assertRaises(ValueError, lambda: self.client.set_param(name="A.LEN", index=None, value=2))
        self.assertRaises(ValueError, lambda: self.client.set_param(name="INIT", index=None, value=1))


class TestOwenModbusClient(unittest.TestCase):
    @patch("pymodbus.client.sync.ModbusSerialClient")
    def setUp(self, mock_modbus):
        self.client = OwenModbusClient(transport=mock_modbus,
                                       device=test_device,
                                       unit=1)

    def test_connect(self):
        self.assertTrue(self.client.connect())

    def test__error_check(self):
        self.assertIsNone(self.client._error_check(retcode=None))
        self.assertTrue(self.client._error_check(retcode=1))

    # TODO: add get_param, set_param test


if __name__ == "__main__":
    unittest.main()
