#! /usr/bin/env python3

"""Таблица настроек счетчика импульсов микропроцессорного СИ8."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from owen.device._types import DEVICE

SI8: DEVICE = {
    "owen": {"DCNT": {"type": "DOT0", "index": {None: None}},
             "DSPD": {"type": "DOT0", "index": {None: None}},
             "DTMR": {"type":  "CLK", "index": {None: None}},
            },
}
