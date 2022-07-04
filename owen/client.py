#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Client(object):
    def __init__(self, transport, device, unit):
        self._transport = transport
        self._transport.device = device
        self._transport.unit = unit
        self._transport.connect()

    def __del__(self):
        self._transport.close()

    def __repr__(self):
        return ("Client(transport={}, unit={})".
                 format(self._transport, self._transport.unit))

    def getParam(self, name, index=None):
        return self._transport.getParam(name.upper(), index)

    def setParam(self, name, index=None, value=None):
        return self._transport.setParam(name.upper(), index, value)


__all__ = [ "Client" ]
