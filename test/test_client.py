#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from owen.client import ClientMixin, OwenModbusClient, OwenSerialClient
from owen.device import TRM201


class FakeOwenSerialClient(OwenSerialClient):
    def __init__(self, transport, device, unit, addr_len_8):
        super(FakeOwenSerialClient, self).__init__(transport, device, unit, addr_len_8)

    def bus_exchange(self, packet):
        return {b"#GHHGTMOHHRTO\r": b"#GHGMTMOHJHJGJISSTGTIPLKK\r",         # чтение параметра "DEV" тип "STR"
                b"#GHHGHUTIKGJI\r": b"#GHGHHUTIGGJKGK\r",                   # чтение параметра "A.LEN" тип "U8" без индекса
                b"#GHHIRJURGGGGHQIV\r": b"#GHGJRJURGHGGGGQROU\r",           # чтение параметра "DP" тип "U8" с индексом
                b"#GHHGPVMIJIMK\r": b"#GHGIPVMIGGGHNHIR\r",                 # чтение параметра "ADDR" тип "U16" без индекса
                b"#GHHGROTVJNPQ\r": b"#GHGJROTVKIQJIOOJKN\r",               # чтение параметра "PV" тип "F24" без индекса
                b"#GHHIUSIGGGGGTJIT\r": b"#GHGLUSIGKKJROGGGGGPVUS\r",       # чтение параметра "SL.H" тип "F24" с индексом
                b"#GHHGGIJJRIQN\r": b"#GHGJGIJJKNRKMLLNJK\r",               # чтение параметра "N.ERR" тип "U24"

                b"#GHGHHUTIGGJKGK\r": b"#GHGHHUTIGGJKGK\r",                 # запись параметра "A.LEN" тип "U8" без индекса
                b"#GHGJQLQRGHGGGGPNOJ\r": b"#GHGJQLQRGHGGGGPNOJ\r",         # запись параметра "CMP" тип "U8" с индексом
                b"#GHGIPVMIGGGHNHIR\r": b"#GHGIPVMIGGGHNHIR\r",             # запись параметра "ADDR" тип "U16" без индекса
                b"#GHGJPPKMGGGGGGQMGJ\r": b"#GHGJPPKMGGGGGGQMGJ\r",         # запись параметра "R.OUT" тип "F24" без индекса
                b"#GHGLUSIGKKJROGGGGGPVUS\r": b"#GHGLUSIGKKJROGGGGGPVUS\r", # запись параметра "SL.H" тип "F24" с индексом
                b"#GHGGGGUPJSUL\r": b"",                                    # запись параметра "INIT" тип "U8" без индекса
               }[packet]


class TestClientMixin(unittest.TestCase):
    """ The unittest for ClientMixin. """

    @patch("serial.Serial")
    def setUp(self, mock_serial):
        self.client = ClientMixin(transport=mock_serial, device=TRM201, unit=1)

    def tearDown(self):
        self.client.close()

    def test_connect(self):
        self.assertIsNone(self.client.connect())

    def test_close(self):
        self.assertIsNone(self.client.close())

    def test_check_index(self):
        name = "A.LEN"
        dev = TRM201["Owen"][name]

        # correct index
        self.assertEqual(None, self.client.check_index(name=name, dev=dev, index=None))
        # invalid index
        self.assertRaises(ValueError, lambda: self.client.check_index(name=name, dev=dev, index=1))

    def test_check_value(self):
        name = "DEV"
        dev = TRM201["Owen"][name]

        # correct value
        self.assertIsNone(self.client.check_value(name=name, dev=dev, value=None))
        # invalid value
        self.assertRaises(ValueError, lambda: self.client.check_value(name=name, dev=dev, value=1))

        name = "SP"
        dev = TRM201["Owen"][name]

        # correct value
        self.assertEqual(10.0, self.client.check_value(name=name, dev=dev, value=10.0))
        # invalid value (> max)
        self.assertRaises(ValueError, lambda: self.client.check_value(name=name, dev=dev, value=10000))
        # invalid value (< min)
        self.assertRaises(ValueError, lambda: self.client.check_value(name=name, dev=dev, value=-10000))
        # invalid value
        self.assertRaises(ValueError, lambda: self.client.check_value(name=name, dev=dev, value=None))


class TestOwenSerialClient(unittest.TestCase):
    """ The unittest for OwenSerialClient. """

    @patch("serial.Serial")
    def setUp(self, mock_serial):
        self.client = FakeOwenSerialClient(transport=mock_serial, device=TRM201,
                                           unit=1, addr_len_8=True)

    def tearDown(self):
        self.client.close()

    def test_connect(self):
        self.assertTrue(self.client.connect())

    def test_get_param(self):
        # correct index
        self.assertEqual(0, self.client.get_param(name="A.LEN", index=None))
        self.assertEqual(b"\xd2\xd0\xcc201", self.client.get_param(name="DEV", index=None))
        self.assertEqual(1, self.client.get_param(name="DP", index=0))
        self.assertEqual(1, self.client.get_param(name="ADDR", index=None))
        self.assertEqual(81.578125, self.client.get_param(name="PV", index=0))
        self.assertEqual(750.0, self.client.get_param(name="SL.H", index=0))
        self.assertEqual((71, 46181), self.client.get_param(name="N.ERR", index=None))
        # invalid index
        self.assertRaises(ValueError, lambda: self.client.get_param(name="A.LEN", index=2))

    def test_set_param(self):
        # correct index and value
        self.assertTrue(self.client.set_param(name="A.LEN", index=None, value=0))
        self.assertTrue(self.client.set_param(name="CMP", index=0, value=1))
        self.assertTrue(self.client.set_param(name="ADDR", index=None, value=1))
        self.assertTrue(self.client.set_param(name="R.OUT", index=None, value=0.0))
        self.assertTrue(self.client.set_param(name="SL.H", index=0, value=750.0))
        self.assertIsNone(self.client.set_param(name="INIT", index=None, value=None))
        # invalid index
        self.assertRaises(ValueError, lambda: self.client.set_param(name="A.LEN", index=2, value=0))
        # invalid value
        self.assertRaises(ValueError, lambda: self.client.set_param(name="A.LEN", index=None, value=2))
        self.assertRaises(ValueError, lambda: self.client.set_param(name="INIT", index=None, value=1))


class TestOwenModbusClient(unittest.TestCase):
    """ The unittest for OwenModbusClient. """

    @patch("pymodbus.client.sync.ModbusSerialClient")
    def setUp(self, mock_modbus):
        self.client = OwenModbusClient(transport=mock_modbus, device=TRM201, unit=1)

    def tearDown(self):
        self.client.close()

    def test_connect(self):
        self.assertTrue(self.client.connect())

    def test_check_error(self):
        self.assertIsNone(self.client.check_error(retcode=None))
        self.assertTrue(self.client.check_error(retcode=1))

    def test_set_param(self):
        # correct index and value
        value = 20.0
        self.client.modify_value = MagicMock(return_value=value)
        self.client.socket.write_registers = MagicMock(return_value=bytearray([0x1, 0x10, 0x0, 0x5, 0x0, 0x1, 0x11, 0xc8]))
        self.assertTrue(self.client.set_param(name="SP", index=0, value=value))
        # invalid index
        self.assertRaises(ValueError, lambda: self.client.set_param(name="SP", index=2, value=value))
        # invalid value
        self.assertRaises(ValueError, lambda: self.client.set_param(name="SP", index=0, value=None))

    def test_get_param(self):
        # correct index
        self.client._read = MagicMock(return_value=bytearray([0x1, 0x3, 0x2, 0x0, 0x1, 0x79, 0x84]))
        self.client.modify_value = MagicMock(return_value=20.0)
        self.assertEqual(20.0, self.client.get_param(name="SP", index=0))
        # invalid index
        self.assertRaises(ValueError, lambda: self.client.get_param(name="SP", index=2))


if __name__ == "__main__":
    unittest.main()
