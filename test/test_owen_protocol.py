#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from serial import Serial
from owen.protocol import Owen


class TRM(Owen):
    def __init__(self, client, unit):
        Owen.__init__(self, client, unit)
        self.client = client
        self.unit = unit

    def _getPingPong(self, flag, name, index, data=None):
        nhash = self._name2hash(name)
        if data is None: data = []
        if index is not None: data.extend([index>>8 & 0xFF, index & 0xFF])

        packet = self._makepacket(address=self.unit, flag=flag, cmd=nhash, data=data)

        if name == "DEV" and flag:      answer = b'#GHGMTMOHJHJGJISSTGTIPLKK\r'
        elif name == "A.LEn" and flag:  answer = b'#GHGHHUTIGGJKGK\r'
        elif name == "Addr" and flag:   answer = b'#GHGIPVMIGGGHNHIR\r'
        elif name == "SL.H" and flag:   answer = b'#GHGLUSIGKKQIOGGGGGULNP\r'
        elif name == "N.ERR" and flag:  answer = b'#GHGJGIJJGGGGGGNILN\r'

        elif name == "A.LEn" and not flag:  answer = b'#GHGHHUTIGGJKGK\r'
        elif name == "Addr" and not flag:   answer = b'#GHGIPVMIGGGHNHIR\r'
        elif name == "SL.H" and not flag:   answer = b'#GHGLUSIGKKQIOGGGGGULNP\r'

        return answer==packet or self._parse_resp(answer, name)


class OwenProtocolTest(unittest.TestCase):
    ''' This is the unittest for Owen protocol '''

    def setUp(self):
        client = Serial(port=None)
        self.trm = TRM(client=client, unit=1)

    def tearDown(self):
        del self.trm

# Функции расчета хеш-суммы

    def test_fastCalc(self):
        self.assertEqual(20158, self.trm._fastCalc(84, 159, 7))

    def test_owenCRC16(self):
        self.assertEqual(16434, self.trm._owenCRC16([1, 16, 30, 210]))

    def test_owenHash(self):
        self.assertEqual(7890, self.trm._owenHash([21, 42, 28, 46]))

    def test_name2hash(self):
        self.assertEqual(60448, self.trm._name2hash("SL.H"))

# Функции упаковки/распаковки пакетов

    def test_bytes2ascii(self):
        self.assertEqual("#GHHGHUTIKGJI\r", self.trm._bytes2ascii([1, 16, 30, 210, 64, 50]))

    def test_ascii2bytes(self):
        self.assertEqual([1, 1, 30, 210, 0, 52, 4], self.trm._ascii2bytes("#GHGHHUTIGGJKGK\r"))

# Функции упаковки/распаковки данных

    def test_packValue(self):
        self.assertEqual(bytearray([66, 246, 233, 223]), self.trm._packValue("F32", 123.45678))
        self.assertEqual(bytearray([66, 246, 233]), self.trm._packValue("F24", 123.45678))
        self.assertEqual(bytearray([4, 210]), self.trm._packValue("U16", 1234))
        self.assertEqual(bytearray([251, 46]), self.trm._packValue("I16", -1234))
        self.assertEqual(bytearray([12]), self.trm._packValue("U8", 12))
        self.assertEqual(bytearray([244]), self.trm._packValue("I8", -12))
        self.assertEqual(bytearray([84, 83, 69, 84]), self.trm._packValue("STR", b"TEST"))

    def test_unpackValue(self):
        self.assertEqual(123.45677947998047, self.trm._unpackValue("F32", bytearray([66, 246, 233, 223])))
        self.assertEqual(123.455078125, self.trm._unpackValue("F24", bytearray([66, 246, 233])))
        self.assertEqual((0,0), self.trm._unpackValue("U24", bytearray([0, 0, 0])))
        self.assertEqual(1234, self.trm._unpackValue("U16", bytearray([4, 210])))
        self.assertEqual(-1234, self.trm._unpackValue("I16", bytearray([251, 46])))
        self.assertEqual(12, self.trm._unpackValue("U8", bytearray([12])))
        self.assertEqual(-12, self.trm._unpackValue("I8", bytearray([244])))
        self.assertEqual(b"TEST", self.trm._unpackValue("STR", bytearray([84, 83, 69, 84])))

# Функции формирования/разбора пакетов

    def test_makePacket(self):
        self.assertEqual(b"#GHHGHUTIKGJI\r", self.trm._makepacket(1, 1, 7890, []))

    def test_parseResp(self):
        self.assertEqual(bytearray([0]), self.trm._parse_resp(b"#GHGHHUTIGGJKGK\r", "A.LEn"))

# Функции чтения данных

    def test_getParam(self):
        self.assertEqual(b'\xd2\xd0\xcc201', self.trm.getParam(frmt="STR", name="DEV"))
        self.assertEqual(0, self.trm.getParam(frmt="U8", name="A.LEn"))
        self.assertEqual(1, self.trm.getParam(frmt="U16", name="Addr"))
        self.assertEqual(1300.0, self.trm.getParam(frmt="F24", name="SL.H", index=0))
        self.assertEqual((0,0), self.trm.getParam(frmt="U24", name="N.ERR"))

# Функции записи данных

    def test_setParam(self):
        self.assertEqual(True, self.trm.setParam(frmt="U8", name="A.LEn", index=None, value=0))
        self.assertEqual(True, self.trm.setParam(frmt="U16", name="Addr", index=None, value=1))
        self.assertEqual(True, self.trm.setParam(frmt="F24", name="SL.H", index=0, value=1300.0))


if __name__ == "__main__":
    unittest.main()
