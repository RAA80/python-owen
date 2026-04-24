#! /usr/bin/env python3

"""Таблица настроек тахометра ТХ01-RS."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from owen.device._types import DEVICE

TH01: DEVICE = {
    "modbus": {"S.PRO":  {"type":   "U8", "index": {None: 0x0008}, "dp": None, "precision": 0},
               "BPS":    {"type":   "U8", "index": {None: 0x0009}, "dp": None, "precision": 0},
               "LEN":    {"type":   "U8", "index": {None: 0x000A}, "dp": None, "precision": 0},
               "PRTY":   {"type":   "U8", "index": {None: 0x000C}, "dp": None, "precision": 0},
               "SBIT":   {"type":   "U8", "index": {None: 0x000B}, "dp": None, "precision": 0},
               "ADDR":   {"type":  "U16", "index": {None: 0x0006}, "dp": None, "precision": 0},
               "RS.DL":  {"type":   "U8", "index": {None: 0x000D}, "dp": None, "precision": 0},
               "OUTDAC": {"type":   "U8", "index": {None: 0x0031}, "dp": None, "precision": 0},
               "UDAC":   {"type":  "U32", "index": {None: 0x0032}, "dp": None, "precision": 0},
               "DPRO":   {"type":  "U32", "index": {None: 0x0034}, "dp": None, "precision": 0},
               "LOR":    {"type":  "U32", "index": {None: 0x0036}, "dp": None, "precision": 0},
               "HIR":    {"type":  "U32", "index": {None: 0x0038}, "dp": None, "precision": 0},
               "OFFDAC": {"type":   "U8", "index": {None: 0x003A}, "dp": None, "precision": 0},
               "SRCC":   {"type":   "U8", "index": {None: 0x0013}, "dp": None, "precision": 0},
               "OUTDO":  {"type":   "U8", "index": {None: 0x0014}, "dp": None, "precision": 0},
               "DOBLK":  {"type":   "U8", "index": {None: 0x0015}, "dp": None, "precision": 0},
               "DODELA": {"type":  "U16", "index": {None: 0x0016}, "dp": None, "precision": 0},
               "UDO":    {"type":  "U32", "index": {None: 0x0017}, "dp": None, "precision": 0},
               "DU":     {"type":  "U32", "index": {None: 0x0019}, "dp": None, "precision": 0},
               "UDAY":   {"type":  "U16", "index": {None: 0x001B}, "dp": None, "precision": 0},
               "UHOUR":  {"type":   "U8", "index": {None: 0x001C}, "dp": None, "precision": 0},
               "UMIN":   {"type":   "U8", "index": {None: 0x001D}, "dp": None, "precision": 0},
               "USEC":   {"type":   "U8", "index": {None: 0x001E}, "dp": None, "precision": 0},
               "OFFDO":  {"type":   "U8", "index": {None: 0x001F}, "dp": None, "precision": 0},
               "DTTA":   {"type":   "U8", "index": {None: 0x0020}, "dp": None, "precision": 0},
               "MAV.L":  {"type":   "U8", "index": {None: 0x0021}, "dp": None, "precision": 0},
               "DP":     {"type":   "U8", "index": {None: 0x0022}, "dp": None, "precision": 0},
               "FDP":    {"type":   "U8", "index": {None: 0x0023}, "dp": None, "precision": 0},
               "F":      {"type":  "U16", "index": {None: 0x0024}, "dp": None, "precision": 0},
               "FREQ":   {"type":  "U32", "index": {None: 0x0025}, "dp": None, "precision": 0},
               "MINIMP": {"type":  "U32", "index": {None: 0x0040}, "dp": None, "precision": 0},
               "PASS":   {"type":  "U32", "index": {None: 0x0027}, "dp": None, "precision": 0},
               "PV":     {"type":  "U32", "index": {None: 0x0029}, "dp": None, "precision": 0},
               "TIME":   {"type":  "U32", "index": {None: 0x002B}, "dp": None, "precision": 0},
               "OST":    {"type":   "U8", "index": {None: 0x002D}, "dp": None, "precision": 0},
               "IST":    {"type":   "U8", "index": {None: 0x002E}, "dp": None, "precision": 0},
               "DEV":    {"type": "STR6", "index": {None: 0x0000}, "dp": None, "precision": 0},
               "VER":    {"type": "STR6", "index": {None: 0x0003}, "dp": None, "precision": 0},
               "VAR":    {"type":   "U8", "index": {None: 0x0012}, "dp": None, "precision": 0},
               "RES.T":  {"type":   "U8", "index": {None: 0x002F}, "dp": None, "precision": 0},
               "DEFAUL": {"type":   "U8", "index": {None: 0x0030}, "dp": None, "precision": 0},
               "APPLY":  {"type":   "U8", "index": {None: 0x000F}, "dp": None, "precision": 0},
              },
    "byteorder": ">",
    "wordorder": ">",
}
