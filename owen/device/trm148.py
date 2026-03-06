#! /usr/bin/env python3

"""Таблица настроек измерителя регулятора микропроцессорного ТРМ148."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pymodbus.constants import Endian

if TYPE_CHECKING:
    from owen.device._types import DEVICE

TRM148: DEVICE = {
    "owen": {"READ":  {"type": "F32+T", "index": {None: None}},
             "R.CAL": {"type": "F32+T", "index": {None: None}},
             "CAL.T": {"type":    "U8", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "SP.LU": {"type":  "SDOT", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "P.-SP": {"type":    "U8", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "VER":   {"type":   "STR", "index": {None: None}},
             "DEV":   {"type":   "STR", "index": {None: None}},
             "MOD.V": {"type":    "U8", "index": {None: None}},
            },
    "modbus": {"R.ST":   {"type": "U16", "index": {0: 0x0060, 1: 0x0061, 2: 0x0062, 3: 0x0063, 4: 0x0064, 5: 0x0065, 6: 0x0066, 7: 0x0067}, "dp": None, "precision": 0},
               "IN.T":   {"type": "U16", "index": {0: 0x0100, 1: 0x0101, 2: 0x0102, 3: 0x0103, 4: 0x0104, 5: 0x0105, 6: 0x0106, 7: 0x0107}, "dp": None, "precision": 0},
               "IN.FD":  {"type": "U16", "index": {0: 0x0110, 1: 0x0111, 2: 0x0112, 3: 0x0113, 4: 0x0114, 5: 0x0115, 6: 0x0116, 7: 0x0117}, "dp": None, "precision": 0},
               "IN.FG":  {"type": "F32", "index": {0: 0x0120, 1: 0x0122, 2: 0x0124, 3: 0x0126, 4: 0x0128, 5: 0x012A, 6: 0x012C, 7: 0x012E}, "dp": None, "precision": 0},
               "ITRL":   {"type": "F32", "index": {0: 0x0130, 1: 0x0132, 2: 0x0134, 3: 0x0136, 4: 0x0138, 5: 0x013A, 6: 0x013C, 7: 0x013E}, "dp": None, "precision": 0},
               "IN.SH":  {"type": "F32", "index": {0: 0x0140, 1: 0x0142, 2: 0x0144, 3: 0x0146, 4: 0x0148, 5: 0x014A, 6: 0x014C, 7: 0x014E}, "dp": None, "precision": 0},
               "IN.SL":  {"type": "F32", "index": {0: 0x0150, 1: 0x0152, 2: 0x0154, 3: 0x0156, 4: 0x0158, 5: 0x015A, 6: 0x015C, 7: 0x015E}, "dp": None, "precision": 0},
               "AIN.L":  {"type": "F32", "index": {0: 0x0160, 1: 0x0162, 2: 0x0164, 3: 0x0166, 4: 0x0168, 5: 0x016A, 6: 0x016C, 7: 0x016E}, "dp": None, "precision": 0},
               "AIN.H":  {"type": "F32", "index": {0: 0x0170, 1: 0x0172, 2: 0x0174, 3: 0x0176, 4: 0x0178, 5: 0x017A, 6: 0x017C, 7: 0x017E}, "dp": None, "precision": 0},
               "A.IST":  {"type": "F32", "index": {0: 0x0200, 1: 0x0202, 2: 0x0204, 3: 0x0206, 4: 0x0208, 5: 0x020A, 6: 0x020C, 7: 0x020E}, "dp": None, "precision": 0},
               "REG.T":  {"type": "U16", "index": {0: 0x0300, 1: 0x0301, 2: 0x0302, 3: 0x0303, 4: 0x0304, 5: 0x0305, 6: 0x0306, 7: 0x0307}, "dp": None, "precision": 0},
               "LBA":    {"type": "U16", "index": {0: 0x0310, 1: 0x0311, 2: 0x0312, 3: 0x0313, 4: 0x0314, 5: 0x0315, 6: 0x0316, 7: 0x0317}, "dp": None, "precision": 0},
               "PB":     {"type": "F32", "index": {0: 0x0320, 1: 0x0322, 2: 0x0324, 3: 0x0326, 4: 0x0328, 5: 0x032A, 6: 0x032C, 7: 0x032E}, "dp": None, "precision": 0},
               "TI":     {"type": "U16", "index": {0: 0x0330, 1: 0x0331, 2: 0x0332, 3: 0x0333, 4: 0x0334, 5: 0x0335, 6: 0x0336, 7: 0x0337}, "dp": None, "precision": 0},
               "TD.TI":  {"type": "F32", "index": {0: 0x0340, 1: 0x0342, 2: 0x0344, 3: 0x0346, 4: 0x0348, 5: 0x034A, 6: 0x034C, 7: 0x034E}, "dp": None, "precision": 0},
               "I.UPR":  {"type": "F32", "index": {0: 0x0350, 1: 0x0352, 2: 0x0354, 3: 0x0356, 4: 0x0358, 5: 0x035A, 6: 0x035C, 7: 0x035E}, "dp": None, "precision": 0},
               "I.MIN":  {"type": "F32", "index": {0: 0x0360, 1: 0x0362, 2: 0x0364, 3: 0x0366, 4: 0x0368, 5: 0x036A, 6: 0x036C, 7: 0x036E}, "dp": None, "precision": 0},
               "HYS.C":  {"type": "F32", "index": {0: 0x0370, 1: 0x0372, 2: 0x0374, 3: 0x0376, 4: 0x0378, 5: 0x037A, 6: 0x037C, 7: 0x037E}, "dp": None, "precision": 0},
               "P.RES":  {"type": "F32", "index": {0: 0x0400, 1: 0x0402, 2: 0x0404, 3: 0x0406, 4: 0x0408, 5: 0x040A, 6: 0x040C, 7: 0x040E}, "dp": None, "precision": 0},
               "P.UPR":  {"type": "F32", "index": {0: 0x0410, 1: 0x0412, 2: 0x0414, 3: 0x0416, 4: 0x0418, 5: 0x041A, 6: 0x041C, 7: 0x041E}, "dp": None, "precision": 0},
               "P.MIN":  {"type": "F32", "index": {0: 0x0420, 1: 0x0422, 2: 0x0424, 3: 0x0426, 4: 0x0428, 5: 0x042A, 6: 0x042C, 7: 0x042E}, "dp": None, "precision": 0},
               "DLP":    {"type": "U16", "index": {0: 0x0500, 1: 0x0501, 2: 0x0502, 3: 0x0503, 4: 0x0504, 5: 0x0505, 6: 0x0506, 7: 0x0507}, "dp": None, "precision": 0},
               "DB.F":   {"type": "F32", "index": {0: 0x0510, 1: 0x0512, 2: 0x0514, 3: 0x0516, 4: 0x0518, 5: 0x051A, 6: 0x051C, 7: 0x051E}, "dp": None, "precision": 0},
               "T.STP":  {"type": "U16", "index": {0: 0x0520, 1: 0x0521, 2: 0x0522, 3: 0x0523, 4: 0x0524, 5: 0x0525, 6: 0x0526, 7: 0x0527}, "dp": None, "precision": 0},
               "TP.L":   {"type": "F32", "index": {0: 0x0530, 1: 0x0532, 2: 0x0534, 3: 0x0536, 4: 0x0538, 5: 0x053A, 6: 0x053C, 7: 0x053E}, "dp": None, "precision": 0},
               "TP.H":   {"type": "U16", "index": {0: 0x0540, 1: 0x0541, 2: 0x0542, 3: 0x0543, 4: 0x0544, 5: 0x0545, 6: 0x0546, 7: 0x0547}, "dp": None, "precision": 0},
               "TFP":    {"type": "F32", "index": {0: 0x0550, 1: 0x0552, 2: 0x0554, 3: 0x0556, 4: 0x0558, 5: 0x055A, 6: 0x055C, 7: 0x055E}, "dp": None, "precision": 0},
               "LSP":    {"type": "F32", "index": {0: 0x0560, 1: 0x0562, 2: 0x0564, 3: 0x0566, 4: 0x0568, 5: 0x056A, 6: 0x056C, 7: 0x056E}, "dp": None, "precision": 0},
               "THP":    {"type": "U16", "index": {0: 0x0600, 1: 0x0601, 2: 0x0602, 3: 0x0603, 4: 0x0604, 5: 0x0605, 6: 0x0606, 7: 0x0607}, "dp": None, "precision": 0},
               "T.L":    {"type": "F32", "index": {0: 0x0610, 1: 0x0612, 2: 0x0614, 3: 0x0616, 4: 0x0618, 5: 0x061A, 6: 0x061C, 7: 0x061E}, "dp": None, "precision": 0},
               "AO.L":   {"type": "F32", "index": {0: 0x0620, 1: 0x0622, 2: 0x0624, 3: 0x0626, 4: 0x0628, 5: 0x062A, 6: 0x062C, 7: 0x062E}, "dp": None, "precision": 0},
               "AO.H":   {"type": "F32", "index": {0: 0x0630, 1: 0x0632, 2: 0x0634, 3: 0x0636, 4: 0x0638, 5: 0x063A, 6: 0x063C, 7: 0x063E}, "dp": None, "precision": 0},
               "ER.ST":  {"type": "U16", "index": {0: 0x0640, 1: 0x0641, 2: 0x0642, 3: 0x0643, 4: 0x0644, 5: 0x0645, 6: 0x0646, 7: 0x0647}, "dp": None, "precision": 0},
               "D.LBA":  {"type": "F32", "index": {0: 0x0650, 1: 0x0652, 2: 0x0654, 3: 0x0656, 4: 0x0658, 5: 0x065A, 6: 0x065C, 7: 0x065E}, "dp": None, "precision": 0},
               "T.LBA":  {"type": "U16", "index": {0: 0x0660, 1: 0x0661, 2: 0x0662, 3: 0x0663, 4: 0x0664, 5: 0x0665, 6: 0x0666, 7: 0x0667}, "dp": None, "precision": 0},
               "BPS":    {"type": "U16", "index": {None: 0x1000}, "dp": None, "precision": 0},
               "A.LEN":  {"type": "U16", "index": {None: 0x1004}, "dp": None, "precision": 0},
               "ADDR":   {"type": "U16", "index": {None: 0x1005}, "dp": None, "precision": 0},
               "RS.DL":  {"type": "U16", "index": {None: 0x1006}, "dp": None, "precision": 0},
               "LEN":    {"type": "U16", "index": {None: 0x1001}, "dp": None, "precision": 0},
               "PRTY":   {"type": "U16", "index": {None: 0x1002}, "dp": None, "precision": 0},
               "SBIT":   {"type": "U16", "index": {None: 0x1003}, "dp": None, "precision": 0},
               "OR.SP":  {"type": "U16", "index": {0: 0x0700, 1: 0x0701, 2: 0x0702, 3: 0x0703, 4: 0x0704, 5: 0x0705, 6: 0x0706, 7: 0x0707, 8: 0x0708, 9: 0x0709, 10: 0x070A, 11: 0x070B, 12: 0x070C, 13: 0x070D, 14: 0x070E, 15: 0x070F, 16: 0x0710, 17: 0x0711, 18: 0x0712, 19: 0x0713, 20: 0x0714, 21: 0x0715, 22: 0x0716, 23: 0x0717}, "dp": None, "precision": 0},
               "LF.LU":  {"type": "F32", "index": {0: 0x0720, 1: 0x0722, 2: 0x0724, 3: 0x0726, 4: 0x0728, 5: 0x072A, 6: 0x072C, 7: 0x072E, 8: 0x0730, 9: 0x0732, 10: 0x0734, 11: 0x0736, 12: 0x0738, 13: 0x073A, 14: 0x073C, 15: 0x073E, 16: 0x0740, 17: 0x0742, 18: 0x0744, 19: 0x0746, 20: 0x0748, 21: 0x074A, 22: 0x074C, 23: 0x074E}, "dp": None, "precision": 0},
               "SP.LU":  {"type": "F32", "index": {0: 0x0750, 1: 0x0752, 2: 0x0754, 3: 0x0756, 4: 0x0758, 5: 0x075A, 6: 0x075C, 7: 0x075E, 8: 0x0760, 9: 0x0762, 10: 0x0764, 11: 0x0766, 12: 0x0768, 13: 0x076A, 14: 0x076C, 15: 0x076E, 16: 0x0770, 17: 0x0772, 18: 0x0774, 19: 0x0776, 20: 0x0778, 21: 0x077A, 22: 0x077C, 23: 0x077E}, "dp": None, "precision": 0},
               "B.CH.L": {"type": "F32", "index": {0: 0x0780, 1: 0x0782, 2: 0x0784, 3: 0x0786, 4: 0x0788, 5: 0x078A, 6: 0x078C, 7: 0x078E, 8: 0x0790, 9: 0x0792, 10: 0x0794, 11: 0x0796, 12: 0x0798, 13: 0x079A, 14: 0x079C, 15: 0x079E, 16: 0x07A0, 17: 0x07A2, 18: 0x07A4, 19: 0x07A6, 20: 0x07A8, 21: 0x07AA, 22: 0x07AC, 23: 0x07AE}, "dp": None, "precision": 0},
               "B.CH.H": {"type": "F32", "index": {0: 0x07B0, 1: 0x07B2, 2: 0x07B4, 3: 0x07B6, 4: 0x07B8, 5: 0x07BA, 6: 0x07BC, 7: 0x07BE, 8: 0x07C0, 9: 0x07C2, 10: 0x07C4, 11: 0x07C6, 12: 0x07C8, 13: 0x07CA, 14: 0x07CC, 15: 0x07CE, 16: 0x07D0, 17: 0x07D2, 18: 0x07D4, 19: 0x07D6, 20: 0x07D8, 21: 0x07DA, 22: 0x07DC, 23: 0x07DE}, "dp": None, "precision": 0},
               "ABSC":   {"type": "F32", "index": {0: 0x0800, 1: 0x0802, 2: 0x0804, 3: 0x0806, 4: 0x0808, 5: 0x080A, 6: 0x080C, 7: 0x080E, 8: 0x0810, 9: 0x0812, 10: 0x0814, 11: 0x0816, 12: 0x0818, 13: 0x081A, 14: 0x081C, 15: 0x081E, 16: 0x0820, 17: 0x0822, 18: 0x0824, 19: 0x0826}, "dp": None, "precision": 0},
               "ORDN":   {"type": "F32", "index": {0: 0x0900, 1: 0x0902, 2: 0x0904, 3: 0x0906, 4: 0x0908, 5: 0x090A, 6: 0x090C, 7: 0x090E, 8: 0x0910, 9: 0x0912, 10: 0x0914, 11: 0x0916, 12: 0x0918, 13: 0x091A, 14: 0x091C, 15: 0x091E, 16: 0x0920, 17: 0x0922, 18: 0x0924, 19: 0x0926}, "dp": None, "precision": 0},
              },
    "byteorder": Endian.Big,
    "wordorder": Endian.Big,
}
