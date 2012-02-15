#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# munin.client - client for munin
#
# Copyright © 2012  Julien Danjou <julien@danjou.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import socket

class Client(object):
    def __init__(self, host, port=4949):
        self.host = host
        self.port = port

    def connect(self):
        self._connection = socket.create_connection((self.host, self.port))
        self._s = self._connection.makefile()
        self.hello_string = self._readline()

    def list(self):
        self._connection.sendall("list\n")
        return self._readline().split(' ')

    def _readline(self):
        return self._s.readline().strip()

    def _iterline(self):
        while True:
            line = self._readline()
            if not line:
                break
            elif line.startswith('#'):
                continue
            elif line == '.':
                break
            yield line

    def fetch(self, key):
        self._connection.sendall("fetch %s\n" % key)
        ret = {}
        for line in self._iterline():
            key, rest = line.split('.', 1)
            prop, value = rest.split(' ', 1)
            if value == 'U':
                value = None
            else:
                value = float(value)
            ret[key] = value
        return ret

    def config(self, key):
        self._connection.sendall("config %s\n" % key)
        ret = {}
        for line in self._iterline():
            if line.startswith('graph_'):
                key, value = line.split(' ', 1)
                ret[key] = value
            else:
                key, rest = line.split('.', 1)
                prop, value = rest.split(' ', 1)
                if not ret.get(key):
                    ret[key] = {}
                ret[key][prop] = value
        return ret

    def nodes(self):
        self._connection.sendall("nodes\n")
        return [ line for line in self._iterline() ]

    def version(self):
        self._connection.sendall("version\n")
        return self._readline()


