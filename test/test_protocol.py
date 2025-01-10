#! /usr/bin/env python3

import unittest

from owen.protocol import Owen, OwenError


class TestOwenProtocol(unittest.TestCase):
    """The unittest for Owen protocol."""

    def setUp(self) -> None:
        self.trm = Owen(unit=1, addr_len_8=True)
        self.trm11 = Owen(unit=400, addr_len_8=False)

    def tearDown(self) -> None:
        del self.trm
        del self.trm11

    def test_fast_calc(self) -> None:
        self.assertEqual(20158, self.trm.fast_calc(84, 159, 7))
        self.assertEqual(5565, self.trm.fast_calc(18, 36695, 8))
        self.assertEqual(53661, self.trm.fast_calc(71, 34988, 8))
        self.assertEqual(60031, self.trm.fast_calc(72, 0, 7))
        self.assertEqual(64238, self.trm.fast_calc(156, 23651, 7))
        self.assertIsInstance(self.trm.fast_calc(156, 23651, 7), int)

    def test_owen_crc16(self) -> None:
        self.assertEqual(16434, self.trm.owen_crc16((1, 16, 30, 210)))
        self.assertEqual(44267, self.trm.owen_crc16((1, 18, 200, 128, 0, 0)))
        self.assertEqual(23007, self.trm.owen_crc16((1, 5, 225, 125, 195, 71, 230, 0, 0)))
        self.assertEqual(40940, self.trm.owen_crc16((1, 5, 236, 32, 68, 59, 128, 0, 0)))
        self.assertEqual(59803, self.trm.owen_crc16((1, 8, 45, 91, 52, 48, 48, 48, 46, 51, 48, 86)))
        self.assertEqual(15584, self.trm.owen_crc16((1, 16, 232, 196)))
        self.assertEqual(38212, self.trm.owen_crc16((1, 6, 214, 129, 49, 48, 50, 204, 208, 210)))
        self.assertIsInstance(self.trm.owen_crc16((1, 6, 214, 129, 49, 48, 50, 204, 208, 210)), int)

    def test_owen_hash(self) -> None:
        self.assertEqual(7890, self.trm.owen_hash((21, 42, 28, 46)))
        self.assertEqual(60448, self.trm.owen_hash((56, 43, 34, 78)))
        self.assertEqual(47327, self.trm.owen_hash((50, 62, 78, 78)))
        self.assertEqual(39238, self.trm.owen_hash((55, 48, 60, 58)))
        self.assertEqual(13800, self.trm.owen_hash((48, 78, 78, 78)))
        self.assertEqual(46941, self.trm.owen_hash((25, 56, 51, 48)))
        self.assertEqual(64104, self.trm.owen_hash((24, 38, 73, 24)))
        self.assertEqual(11410, self.trm.owen_hash((28, 62, 72, 2)))
        self.assertEqual(233, self.trm.owen_hash((36, 46, 36, 58)))
        self.assertIsInstance(self.trm.owen_hash((36, 46, 36, 58)), int)

    def test_name2code(self) -> None:
        self.assertEqual((21, 42, 28, 46), self.trm.name2code("A.LEN"))
        self.assertEqual((56, 43, 34, 78), self.trm.name2code("SL.H"))
        self.assertEqual((50, 62, 78, 78), self.trm.name2code("PV"))
        self.assertEqual((55, 48, 60, 58), self.trm.name2code("R.OUT"))
        self.assertEqual((48, 78, 78, 78), self.trm.name2code("O"))
        self.assertEqual((25, 56, 51, 48), self.trm.name2code("C.SP.O"))
        self.assertEqual((24, 38, 73, 24), self.trm.name2code("CJ-.C"))
        self.assertEqual((28, 62, 72, 2), self.trm.name2code("EV-1"))
        self.assertEqual((36, 46, 36, 58), self.trm.name2code("INIT"))
        self.assertIsInstance(self.trm.name2code("INIT"), tuple)

    def test_encode_frame(self) -> None:
        self.assertEqual(b"#GHHGHUTIKGJI\r", self.trm.encode_frame((1, 16, 30, 210, 64, 50)))
        self.assertEqual(b"#GHGHHUTIGGJKGK\r", self.trm.encode_frame((1, 1, 30, 210, 0, 52, 4)))
        self.assertEqual(b"#GHHISOOGGGGGQSUR\r", self.trm.encode_frame((1, 18, 200, 128, 0, 0, 172, 235)))
        self.assertEqual(b"#GHGJSOOGGGGGGGUQRK\r", self.trm.encode_frame((1, 3, 200, 128, 0, 0, 0, 234, 180)))
        self.assertEqual(b"#GHHIPHGNGGGGKKPV\r", self.trm.encode_frame((1, 18, 145, 7, 0, 0, 68, 159)))
        self.assertEqual(b"#GHGLPHGNKHSOGGGGGGJOMV\r", self.trm.encode_frame((1, 5, 145, 7, 65, 200, 0, 0, 0, 56, 111)))
        self.assertEqual(b"#GHHGHIGJUIMK\r", self.trm.encode_frame((1, 16, 18, 3, 226, 100)))
        self.assertEqual(b"#GHGHHIGJGGIHHO\r", self.trm.encode_frame((1, 1, 18, 3, 0, 33, 24)))
        self.assertIsInstance(self.trm.encode_frame((1, 1, 18, 3, 0, 33, 24)), bytes)

    def test_decode_frame(self) -> None:
        self.assertEqual((1, 1, 30, 210, 0, 52, 4), self.trm.decode_frame(b"#GHGHHUTIGGJKGK\r"))
        self.assertEqual((1, 3, 200, 128, 0, 0, 0, 234, 180), self.trm.decode_frame(b"#GHGJSOOGGGGGGGUQRK\r"))
        self.assertEqual((1, 5, 57, 243, 0, 0, 0, 0, 0, 11, 51), self.trm.decode_frame(b"#GHGLJPVJGGGGGGGGGGGRJJ\r"))
        self.assertEqual((1, 5, 225, 125, 195, 71, 230, 0, 0, 89, 223), self.trm.decode_frame(b"#GHGLUHNTSJKNUMGGGGLPTV\r"))
        self.assertEqual((1, 8, 45, 91, 52, 48, 48, 48, 46, 51, 48, 86, 233, 155), self.trm.decode_frame(b"#GHGOITLRJKJGJGJGIUJJJGLMUPPR\r"))
        self.assertEqual((1, 3, 180, 101, 0, 0, 0, 9, 1), self.trm.decode_frame(b"#GHGJRKMLGGGGGGGPGH\r"))
        self.assertEqual((1, 3, 2, 51, 71, 180, 101, 87, 52), self.trm.decode_frame(b"#GHGJGIJJKNRKMLLNJK\r"))
        self.assertEqual((1, 3, 2, 51, 71, 100, 234, 99, 78), self.trm.decode_frame(b"#GHGJGIJJKNMKUQMJKU\r"))
        self.assertEqual((1, 1, 30, 37, 20, 126, 6), self.trm.decode_frame(b"#GHGHHUILHKNUGM\r"))
        self.assertIsInstance(self.trm.decode_frame(b"#GHGHHUILHKNUGM\r"), tuple)

    def test_pack_value(self) -> None:
        self.assertEqual((194, 71, 255, 167, 15, 225), self.trm.pack_value("F32+T", (-49.99966049194336, 4065)))
        self.assertEqual((66, 246, 233, 223), self.trm.pack_value("F32", 123.45678))
        self.assertEqual((164, 14), self.trm.pack_value("SDOT", -10.38))
        self.assertEqual((29, 172), self.trm.pack_value("SDOT", 350.0))
        self.assertEqual((16, 16, 4), self.trm.pack_value("SDOT", 410.0))
        self.assertEqual((16,), self.trm.pack_value("SDOT", 0.0))
        self.assertEqual((0,), self.trm.pack_value("DOT0", 0))
        self.assertEqual((153,), self.trm.pack_value("DOT0", 99))
        self.assertEqual((3, 4), self.trm.pack_value("DOT0", 304))
        self.assertEqual((9, 135, 101, 67, 33), self.trm.pack_value("DOT0", 987654321))
        self.assertEqual((66, 246, 233), self.trm.pack_value("F24", 123.45678))
        self.assertEqual((4, 210), self.trm.pack_value("U16", 1234))
        self.assertEqual((251, 46), self.trm.pack_value("I16", -1234))
        self.assertEqual((12,), self.trm.pack_value("U8", 12))
        self.assertEqual((244,), self.trm.pack_value("I8", -12))
        self.assertEqual((50, 48, 50, 204, 208, 210), self.trm.pack_value("STR", "ТРМ202"))
        self.assertIsNone(self.trm.pack_value("U8", None))          # if empty buffer
        self.assertIsInstance(self.trm.pack_value("I8", -12), tuple)

    def test_unpack_value(self) -> None:
        self.assertEqual((-49.99966049194336, 4065), self.trm.unpack_value("F32+T", bytes([194, 71, 255, 167, 15, 225]), None))
        self.assertEqual(123.45677947998047, self.trm.unpack_value("F32", bytes([66, 246, 233, 223]), None))
        self.assertEqual(350.0, self.trm.unpack_value("SDOT", bytes([29, 172, 0, 0]), 0))
        self.assertEqual(410.0, self.trm.unpack_value("SDOT", bytes([16, 16, 4, 0, 0]), 0))
        self.assertEqual(350.0, self.trm.unpack_value("SDOT", bytes([29, 172]), None))
        self.assertEqual(410.0, self.trm.unpack_value("SDOT", bytes([16, 16, 4]), None))
        self.assertEqual(0.0, self.trm.unpack_value("SDOT", bytes([16, 0, 0]), 0))
        self.assertEqual(0.0, self.trm.unpack_value("SDOT", bytes([16]), None))
        self.assertEqual(0, self.trm.unpack_value("DOT0", bytes([0]), None))
        self.assertEqual(99, self.trm.unpack_value("DOT0", bytes([153]), None))
        self.assertEqual(304, self.trm.unpack_value("DOT0", bytes([3, 4]), None))
        self.assertEqual(987654321, self.trm.unpack_value("DOT0", bytes([9, 135, 101, 67, 33]), None))
        self.assertEqual(123.455078125, self.trm.unpack_value("F24", bytes([66, 246, 233]), None))
        self.assertEqual((71, 46059), self.trm.unpack_value("U24", bytes([71, 179, 235]), None))
        self.assertEqual(1234, self.trm.unpack_value("U16", bytes([4, 210]), None))
        self.assertEqual(-1234, self.trm.unpack_value("I16", bytes([251, 46]), None))
        self.assertEqual(12, self.trm.unpack_value("U8", bytes([12]), None))
        self.assertEqual(-12, self.trm.unpack_value("I8", bytes([244]), None))
        self.assertEqual("ТРМ202", self.trm.unpack_value("STR", bytes([50, 48, 50, 204, 208, 210]), None))
        self.assertRaises(OwenError, lambda: self.trm.unpack_value("F32", bytes([253]), None))  # if error code

    def test_make_packet(self) -> None:
        self.assertEqual(b"#GHHGHUTIKGJI\r", self.trm.make_packet(1, "A.LEN", None, None))
        self.assertEqual(b"#GHHISOOGGGGGQSUR\r", self.trm.make_packet(1, "DON", 0, None))
        self.assertEqual(b"#GHGLJPVJGGGGGGGGGGGRJJ\r", self.trm.make_packet(0, "FB", 0, (0, 0, 0)))
        self.assertEqual(b"#GHGLUHNTSJKNUMGGGGLPTV\r", self.trm.make_packet(0, "SL.L", 0, (195, 71, 230)))
        self.assertEqual(b"#GHGHRNIUGGMJSQ\r", self.trm.make_packet(0, "SBIT", None, (0,)))
        self.assertEqual(b"#GHGLPHGNKHSOGGGGGGJOMV\r", self.trm.make_packet(0, "SP", 0, (65, 200, 0)))
        self.assertEqual(b"#GHGHRNMGGORMUL\r", self.trm.make_packet(0, "BPS", None, (8,)))

        self.assertEqual(b"#JIHIPHGNGGGGJHVJ\r", self.trm11.make_packet(1, "SP", 0, None))
        self.assertEqual(b"#JIGLPHGNKHRHPQGGGGUMHO\r", self.trm11.make_packet(0, "SP", 0, (65, 177, 154)))
        self.assertIsInstance(self.trm11.make_packet(0, "SP", 0, (65, 177, 154)), bytes)

    def test_parse_response(self) -> None:
        self.assertEqual(bytes([0]), self.trm.parse_response(b"#GHHGHUTIKGJI\r", b"#GHGHHUTIGGJKGK\r"))
        self.assertEqual(bytes([0, 0, 0]), self.trm.parse_response(b"#GHHISOOGGGGGQSUR\r", b"#GHGJSOOGGGGGGGUQRK\r"))
        self.assertEqual(bytes([195, 71, 230, 0, 0]), self.trm.parse_response(b"#GHHIUHNTGGGGPULL\r", b"#GHGLUHNTSJKNUMGGGGLPTV\r"))
        self.assertEqual(bytes([52, 48, 48, 48, 46, 51, 48, 86]), self.trm.parse_response(b"#GHHGITLRRKVN\r", b"#GHGOITLRJKJGJGJGIUJJJGLMUPPR\r"))
        self.assertEqual(bytes([71, 180, 101]), self.trm.parse_response(b"#GHHGGIJJRIQN\r", b"#GHGJGIJJKNRKMLLNJK\r"))
        self.assertEqual(bytes([100]), self.trm.parse_response(b"#GHHGJONIJKMN\r", b"#GHGHJONIMKKIMP\r"))
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHGHUTIKGJI\r", b""))                                 # if empty message
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHGHUTIKGJI\r", b"GHHGHUTIKGJI\r"))                   # if first byte not '#'
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHGHUTIKGJI\r", b"#GHHGHUTIKGJI"))                    # if last byte not '\r'
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHINNRQGGGGRUIR\r", b"#GHGJGIJJKNNNRQPUSV\r"))        # if error code
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHIUHNTGGGGPULL\r", b"#GHGLUHNTSJKNUMGGGGLPTD\r"))    # if checksum error
        self.assertRaises(OwenError, lambda: self.trm.parse_response(b"#GHHGROTVJNPQ\r", b"#IJKJGIJJJHKOKNIJTO\r"))            # if addresses mismatch
        self.assertIsInstance(self.trm.parse_response(b"#GHHGJONIJKMN\r", b"#GHGHJONIMKKIMP\r"), bytes)
        self.assertIsInstance(self.trm.parse_response(b"#GHGLUHNTJVOGGGGGGGQGIG\r", b"#GHGLUHNTJVOGGGGGGGQGIG\r"), bytes)


if __name__ == "__main__":
    unittest.main()
