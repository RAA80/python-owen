#! /usr/bin/env python3

"""Таблица настроек измерителя-регулятора восьмиканального ТРМ138."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pymodbus.constants import Endian

if TYPE_CHECKING:
    from owen.device._types import DEVICE

TRM138: DEVICE = {
    "owen": {"IND.T":  {"type":  "DOT0", "index": {None: None}},
             "IND.R":  {"type":  "DOT0", "index": {None: None}},
             "IND.A":  {"type":    "U8", "index": {None: None}},
             "AL.DR":  {"type":  "DOT0", "index": {None: None}},
             "AL.HD":  {"type":  "DOT0", "index": {None: None}},
             "AL.ST":  {"type":    "U8", "index": {None: None}},
             "CJ-.C":  {"type":    "U8", "index": {None: None}},
             "SYST":   {"type":    "U8", "index": {None: None}},
             "BL.AR":  {"type":    "U8", "index": {None: None}},
             "IN.FD":  {"type":  "DOT0", "index": {None: None}},
             "PRT":    {"type":  "DOT0", "index": {None: None}},
             "IN.SH":  {"type":  "SDOT", "index": {None: None}},
             "IN.SL":  {"type":  "DOT3", "index": {None: None}},
             "IN-T":   {"type":    "U8", "index": {None: None}},
             "IN.FG":  {"type":  "SDOT", "index": {None: None}},
             "AIN.L":  {"type":  "SDOT", "index": {None: None}},
             "AIN.H":  {"type":  "SDOT", "index": {None: None}},
             "C.SP":   {"type":  "SDOT", "index": {None: None}},
             "HYST":   {"type":  "SDOT", "index": {None: None}},
             "C.SP.O": {"type":  "SDOT", "index": {None: None}},
             "HT.ON":  {"type":  "DOT0", "index": {None: None}},
             "HT.OF":  {"type":  "DOT0", "index": {None: None}},
             "DL.ON":  {"type":  "DOT0", "index": {None: None}},
             "DL.OF":  {"type":  "DOT0", "index": {None: None}},
             "BL.ST":  {"type":    "U8", "index": {None: None}},
             "DP_":    {"type":  "DOT0", "index": {None: None}},
             "ER.ST":  {"type":    "U8", "index": {None: None}},
             "AL.T":   {"type":  "DOT0", "index": {None: None}},
             "AO.L":   {"type":  "SDOT", "index": {None: None}},
             "AO.H":   {"type":  "SDOT", "index": {None: None}},
             "C.DR":   {"type":  "DOT0", "index": {None: None}},
             "C.LBT":  {"type":  "DOT0", "index": {None: None}},
             "AL.OU":  {"type":    "U8", "index": {None: None}},
             "C.LBA":  {"type":  "SDOT", "index": {None: None}},
             "C.IN":   {"type":  "DOT0", "index": {None: None}},
             "BPS":    {"type":    "U8", "index": {None: None}},
             "LEN":    {"type":    "U8", "index": {None: None}},
             "PRTY":   {"type":    "U8", "index": {None: None}},
             "SBIT":   {"type":    "U8", "index": {None: None}},
             "A.LEN":  {"type":    "U8", "index": {None: None}},
             "ADDR":   {"type":   "U16", "index": {None: None}},
             "N.FLT":  {"type":    "U8", "index": {None: None}},
             "DATA":   {"type":    "U8", "index": {None: None}},
             "T.INC":  {"type":    "U8", "index": {None: None}},
             "CHAR":   {"type":   "STR", "index": {None: None}},
             "SOUR":   {"type":   "U16", "index": {None: None}},
             "READ":   {"type": "F32+T", "index": {None: None}},
             "DR.DG":  {"type":  "DOT0", "index": {None: None}},
             "N.ERR":  {"type":   "U24", "index": {None: None}},
            },
    "modbus": {"READ":   {"type": "F32", "index": {0: 0x0003, 1: 0x0008, 2: 0x000D, 3: 0x0012, 4: 0x0017, 5: 0x001C, 6: 0x0021, 7: 0x0026}, "dp": None, "precision": 0},
               "R.CAL":  {"type": "F32", "index": {0: 0x0043, 1: 0x0048, 2: 0x004D, 3: 0x0052, 4: 0x0057, 5: 0x005C, 6: 0x0061, 7: 0x0066}, "dp": None, "precision": 0},
               "R.CIN":  {"type": "U16", "index": {0: 0x0000, 1: 0x0001, 2: 0x0002, 3: 0x0003, 4: 0x0004, 5: 0x0005, 6: 0x0006, 7: 0x0007}, "dp": None, "precision": 0},
               "C.SP":   {"type": "U16", "index": {0: 0x0011, 1: 0x0015, 2: 0x0019, 3: 0x001D, 4: 0x0021, 5: 0x0025, 6: 0x0029, 7: 0x002D}, "dp": None, "precision": 0},
               "C.SP.S": {"type": "U16", "index": {0: 0x0013, 1: 0x0017, 2: 0x001B, 3: 0x001F, 4: 0x0023, 5: 0x0027, 6: 0x002B, 7: 0x002F}, "dp": None, "precision": 0},
               "HYST":   {"type": "U16", "index": {0: 0x0031, 1: 0x0033, 2: 0x0035, 3: 0x0037, 4: 0x0039, 5: 0x003B, 6: 0x003D, 7: 0x003F}, "dp": None, "precision": 0},
               "C.DR":   {"type": "U16", "index": {0: 0x0041, 1: 0x0042, 2: 0x0043, 3: 0x0044, 4: 0x0045, 5: 0x0046, 6: 0x0047, 7: 0x0048}, "dp": None, "precision": 0},
              },
    "byteorder": Endian.Big,
    "wordorder": Endian.Big,
}
