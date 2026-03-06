#! /usr/bin/env python3

"""Таблица настроек измерителя-регулятора ТРМ151."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from owen.device._types import DEVICE

TRM151: DEVICE = {
    "owen": {"READ":  {"type": "F32+T", "index": {None: None}},
             "R.CAL": {"type": "F32+T", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "RD.RG": {"type":   "F32", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "R.OUT": {"type":   "F32", "index": {0: 0, 1: 1}},
             "SET.P": {"type":   "F32", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "R.KEY": {"type":   "U16", "index": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}},
             "R.PRG": {"type":   "U16", "index": {None: None}},
             "R.STP": {"type":   "U16", "index": {None: None}},
             "R.ST":  {"type":   "U16", "index": {None: None}},
             "R.S":   {"type":   "U16", "index": {None: None}},
            },
}
