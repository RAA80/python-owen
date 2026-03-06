#! /usr/bin/env python3

"""Таблица настроек счетчика импульсов СИ30."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from owen.device._types import DEVICE

SI30: DEVICE = {
    "owen": {"BPS":   {"type": "U16", "index": {None: None}},
             "LEN":   {"type": "U16", "index": {None: None}},
             "PRTY":  {"type": "U16", "index": {None: None}},
             "A.LEN": {"type": "U16", "index": {None: None}},
             "ADDR":  {"type": "U16", "index": {None: None}},
             "RS.DL": {"type": "U16", "index": {None: None}},
             "DP":    {"type": "U16", "index": {None: None}},
             "INP":   {"type": "U16", "index": {None: None}},
             "OUT":   {"type": "U16", "index": {None: None}},
             "SPM":   {"type": "U16", "index": {None: None}},
             "RST":   {"type": "U16", "index": {None: None}},
             "U1":    {"type": "I32", "index": {None: None}},
             "U2":    {"type": "I32", "index": {None: None}},
             "T1":    {"type": "U32", "index": {None: None}},
             "T2":    {"type": "U32", "index": {None: None}},
             "FDP":   {"type": "U16", "index": {None: None}},
             "F":     {"type": "U32", "index": {None: None}},
             "FREQ":  {"type": "U16", "index": {None: None}},
             "CNT.T": {"type": "U32", "index": {None: None}},
             "LOCK":  {"type": "U16", "index": {None: None}},
             "IND2":  {"type": "U16", "index": {None: None}},
             "BRHT":  {"type": "U16", "index": {None: None}},
             "SIG":   {"type": "U16", "index": {None: None}},
             "PASS":  {"type": "U16", "index": {None: None}},
             "CTR":   {"type": "I32", "index": {None: None}},
             "CEU":   {"type": "I32", "index": {None: None}},
             "STST":  {"type": "U16", "index": {None: None}},
             "CUR":   {"type": "U16", "index": {None: None}},
             "N.ERR": {"type": "U16", "index": {None: None}},
             "DEV":   {"type": "STR", "index": {None: None}},
             "VER":   {"type": "STR", "index": {None: None}},
             "RSTI":  {"type":  "U8", "index": {None: None}},
             "LOCI":  {"type":  "U8", "index": {None: None}},
             "OST1":  {"type":  "U8", "index": {None: None}},
             "OST2":  {"type":  "U8", "index": {None: None}},
             "RSTC":  {"type":  "U8", "index": {None: None}},
            },
}
