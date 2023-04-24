#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
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


class TestOwenProtocol(unittest.TestCase):
    ''' This is the unittest for Owen protocol '''

    def setUp(self):
        self.trm = TRM(client=None, unit=1)

    def tearDown(self):
        del self.trm

    def test_fast_calc(self):
        self.assertEqual(20158, self.trm._fast_calc(84, 159, 7))
        self.assertEqual(5565, self.trm._fast_calc(18, 36695, 8))
        self.assertEqual(53661, self.trm._fast_calc(71, 34988, 8))
        self.assertEqual(60031, self.trm._fast_calc(72, 0, 7))
        self.assertEqual(64238, self.trm._fast_calc(156, 23651, 7))

    def test_owen_crc16(self):
        self.assertEqual(16434, self.trm._owen_crc16([1, 16, 30, 210]))
        self.assertEqual(44267, self.trm._owen_crc16([1, 18, 200, 128, 0, 0]))
        self.assertEqual(23007, self.trm._owen_crc16([1, 5, 225, 125, 195, 71, 230, 0, 0]))
        self.assertEqual(40940, self.trm._owen_crc16([1, 5, 236, 32, 68, 59, 128, 0, 0]))
        self.assertEqual(59803, self.trm._owen_crc16([1, 8, 45, 91, 52, 48, 48, 48, 46, 51, 48, 86]))
        self.assertEqual(15584, self.trm._owen_crc16([1, 16, 232, 196]))
        self.assertEqual(38212, self.trm._owen_crc16([1, 6, 214, 129, 49, 48, 50, 204, 208, 210]))

    def test_owen_hash(self):
        self.assertEqual(7890, self.trm._owen_hash([21, 42, 28, 46]))
        self.assertEqual(60448, self.trm._owen_hash([56, 43, 34, 78]))
        self.assertEqual(47327, self.trm._owen_hash([50, 62, 78, 78]))
        self.assertEqual(39238, self.trm._owen_hash([55, 48, 60, 58]))
        self.assertEqual(13800, self.trm._owen_hash([48, 78, 78, 78]))
        self.assertEqual(46941, self.trm._owen_hash([25, 56, 51, 48]))
        self.assertEqual(64104, self.trm._owen_hash([24, 38, 73, 24]))
        self.assertEqual(11410, self.trm._owen_hash([28, 62, 72, 2]))
        self.assertEqual(233, self.trm._owen_hash([36, 46, 36, 58]))

    def test_name2hash(self):
        self.assertEqual(7890, self.trm._name2hash("A.LEN"))
        self.assertEqual(60448, self.trm._name2hash("SL.H"))
        self.assertEqual(47327, self.trm._name2hash("PV"))
        self.assertEqual(39238, self.trm._name2hash("R.OUT"))
        self.assertEqual(13800, self.trm._name2hash("O"))
        self.assertEqual(46941, self.trm._name2hash("C.SP.O"))
        self.assertEqual(64104, self.trm._name2hash("CJ-.C"))
        self.assertEqual(11410, self.trm._name2hash("EV-1"))
        self.assertEqual(233, self.trm._name2hash("INIT"))

    def test_bytes2ascii(self):
        self.assertEqual(b"#GHHGHUTIKGJI\r", self.trm._bytes2ascii([1, 16, 30, 210, 64, 50]))
        self.assertEqual(b"#GHGHHUTIGGJKGK\r", self.trm._bytes2ascii([1, 1, 30, 210, 0, 52, 4]))
        self.assertEqual(b"#GHHISOOGGGGGQSUR\r", self.trm._bytes2ascii([1, 18, 200, 128, 0, 0, 172, 235]))
        self.assertEqual(b"#GHGJSOOGGGGGGGUQRK\r", self.trm._bytes2ascii([1, 3, 200, 128, 0, 0, 0, 234, 180]))
        self.assertEqual(b"#GHHIPHGNGGGGKKPV\r", self.trm._bytes2ascii([1, 18, 145, 7, 0, 0, 68, 159]))
        self.assertEqual(b"#GHGLPHGNKHSOGGGGGGJOMV\r", self.trm._bytes2ascii([1, 5, 145, 7, 65, 200, 0, 0, 0, 56, 111]))
        self.assertEqual(b"#GHHGHIGJUIMK\r", self.trm._bytes2ascii([1, 16, 18, 3, 226, 100]))
        self.assertEqual(b"#GHGHHIGJGGIHHO\r", self.trm._bytes2ascii([1, 1, 18, 3, 0, 33, 24]))

    def test_ascii2bytes(self):
        self.assertEqual([1, 1, 30, 210, 0, 52, 4], self.trm._ascii2bytes("#GHGHHUTIGGJKGK\r"))
        self.assertEqual([1, 3, 200, 128, 0, 0, 0, 234, 180], self.trm._ascii2bytes("#GHGJSOOGGGGGGGUQRK\r"))
        self.assertEqual([1, 5, 57, 243, 0, 0, 0, 0, 0, 11, 51], self.trm._ascii2bytes("#GHGLJPVJGGGGGGGGGGGRJJ\r"))
        self.assertEqual([1, 5, 225, 125, 195, 71, 230, 0, 0, 89, 223], self.trm._ascii2bytes("#GHGLUHNTSJKNUMGGGGLPTV\r"))
        self.assertEqual([1, 8, 45, 91, 52, 48, 48, 48, 46, 51, 48, 86, 233, 155], self.trm._ascii2bytes("#GHGOITLRJKJGJGJGIUJJJGLMUPPR\r"))
        self.assertEqual([1, 3, 180, 101, 0, 0, 0, 9, 1], self.trm._ascii2bytes("#GHGJRKMLGGGGGGGPGH\r"))
        self.assertEqual([1, 3, 2, 51, 71, 180, 101, 87, 52], self.trm._ascii2bytes("#GHGJGIJJKNRKMLLNJK\r"))
        self.assertEqual([1, 3, 2, 51, 71, 100, 234, 99, 78], self.trm._ascii2bytes("#GHGJGIJJKNMKUQMJKU\r"))
        self.assertEqual([1, 1, 30, 37, 20, 126, 6], self.trm._ascii2bytes("#GHGHHUILHKNUGM\r"))

    def test_pack_value(self):
        self.assertEqual([66, 246, 233, 223], self.trm._pack_value("F32", 123.45678))
        self.assertEqual([66, 246, 233], self.trm._pack_value("F24", 123.45678))
        self.assertEqual([4, 210], self.trm._pack_value("U16", 1234))
        self.assertEqual([251, 46], self.trm._pack_value("I16", -1234))
        self.assertEqual([12], self.trm._pack_value("U8", 12))
        self.assertEqual([244], self.trm._pack_value("I8", -12))
        self.assertEqual([84, 83, 69, 84], self.trm._pack_value("STR", b"TEST"))
        self.assertIsNone(self.trm._pack_value("U8", None))                 # if empty buffer

    def test_unpack_value(self):
        self.assertEqual(123.45677947998047, self.trm._unpack_value("F32", bytearray([66, 246, 233, 223])))
        self.assertEqual(123.455078125, self.trm._unpack_value("F24", bytearray([66, 246, 233])))
        self.assertEqual((0,0), self.trm._unpack_value("U24", bytearray([0, 0, 0])))
        self.assertEqual(1234, self.trm._unpack_value("U16", bytearray([4, 210])))
        self.assertEqual(-1234, self.trm._unpack_value("I16", bytearray([251, 46])))
        self.assertEqual(12, self.trm._unpack_value("U8", bytearray([12])))
        self.assertEqual(-12, self.trm._unpack_value("I8", bytearray([244])))
        self.assertEqual(b"TEST", self.trm._unpack_value("STR", bytearray([84, 83, 69, 84])))
        self.assertIsNone(self.trm._unpack_value("U8", None))               # if empty buffer
        self.assertIsNone(self.trm._unpack_value("F32", bytearray([253])))  # if error code

    def test_make_packet(self):
        self.assertEqual(b"#GHHGHUTIKGJI\r", self.trm._make_packet(1, 7890, None, []))
        self.assertEqual(b"#GHHISOOGGGGGQSUR\r", self.trm._make_packet(1, 51328, 0, []))
        self.assertEqual(b"#GHGLJPVJGGGGGGGGGGGRJJ\r", self.trm._make_packet(0, 14835, 0, [0, 0, 0]))
        self.assertEqual(b"#GHGLUHNTSJKNUMGGGGLPTV\r", self.trm._make_packet(0, 57725, 0, [195, 71, 230]))
        self.assertEqual(b"#GHGHRNIUGGMJSQ\r", self.trm._make_packet(0, 46894, None, [0]))
        self.assertEqual(b"#GHGLPHGNKHSOGGGGGGJOMV\r", self.trm._make_packet(0, 37127, 0, [65, 200, 0]))
        self.assertEqual(b"#GHGHRNMGGORMUL\r", self.trm._make_packet(0, 46944, None, [8]))

    def test_parse_response(self):
        self.assertEqual(bytearray([0]), self.trm._parse_response(b"#GHGHHUTIGGJKGK\r", "A.LEn"))
        self.assertEqual(bytearray([0, 0, 0]), self.trm._parse_response(b"#GHGJSOOGGGGGGGUQRK\r", "DON"))
        self.assertEqual(bytearray([195, 71, 230, 0, 0]), self.trm._parse_response(b"#GHGLUHNTSJKNUMGGGGLPTV\r", "SL.L"))
        self.assertEqual(bytearray([52, 48, 48, 48, 46, 51, 48, 86]), self.trm._parse_response(b"#GHGOITLRJKJGJGJGIUJJJGLMUPPR\r", "VER"))
        self.assertEqual(bytearray([71, 180, 101]), self.trm._parse_response(b"#GHGJGIJJKNRKMLLNJK\r", "N.ERR"))
        self.assertEqual(bytearray([100]), self.trm._parse_response(b"#GHGHJONIMKKIMP\r", "REST"))
        self.assertIsNone(self.trm._parse_response(b"", "A.LEn"))                           # if empty message
        self.assertIsNone(self.trm._parse_response(b"#GHGJGIJJKNNNRQPUSV\r", "CTL"))        # if error code
        self.assertIsNone(self.trm._parse_response(b"#GHGLUHNTSJKNUMGGGGLPTD\r", "SL.L"))   # if checksum error

    def test_get_param(self):
        self.assertEqual(b'\xd2\xd0\xcc201', self.trm.get_param(frmt="STR", name="DEV"))
        self.assertEqual(0, self.trm.get_param(frmt="U8", name="A.LEN"))
        self.assertEqual(1, self.trm.get_param(frmt="U8", name="DP", index=0))
        self.assertEqual(1, self.trm.get_param(frmt="U16", name="ADDR"))
        self.assertEqual(81.578125, self.trm.get_param(frmt="F24", name="PV"))
        self.assertEqual(750.0, self.trm.get_param(frmt="F24", name="SL.H", index=0))
        self.assertEqual((71, 46181), self.trm.get_param(frmt="U24", name="N.ERR"))

    def test_set_param(self):
        self.assertTrue(self.trm.set_param(frmt="U8", name="A.LEN", index=None, value=0))
        self.assertTrue(self.trm.set_param(frmt="U8", name="CMP", index=0, value=1))
        self.assertTrue(self.trm.set_param(frmt="U16", name="ADDR", index=None, value=1))
        self.assertTrue(self.trm.set_param(frmt="F24", name="R.OUT", index=None, value=0.0))
        self.assertTrue(self.trm.set_param(frmt="F24", name="SL.H", index=0, value=750.0))


if __name__ == "__main__":
    unittest.main()
