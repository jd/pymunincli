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
from itertools import groupby, imap
from operator import itemgetter

def _itergraph(plugin, i):
    def itergraph():
        graph = plugin
        for line in i:
            if line.startswith("multigraph "):
                graph = line.split()[1]
            else:
                yield graph, line

    for graph, graph_line in groupby(itergraph(), key=itemgetter(0)):
        yield graph, imap(itemgetter(1), graph_line)

class ClientError(Exception):
    pass

class Client(object):
    def __init__(self, host, port=4949):
        self.host = host
        self.port = port
        self.buffer = ""

    def connect(self):
        self._connection = socket.create_connection((self.host, self.port))
        self.hello_string = self._readline()

        self._connection.sendall("cap multigraph\n")
        self.cap_list = self._readline().split()[1:]

    def list(self):
        self._connection.sendall("list\n")
        return self._readline().split(' ')

    def _readline(self):
        while '\n' not in self.buffer:
            s = self._connection.recv(4096)
            if not s:
                raise ClientError("server unexpectedly closed connection")

            self.buffer += s

        r, self.buffer = self.buffer.split('\n', 1)
        return r.strip()

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

    def _itergraph(self, key):
        return _itergraph(key, self._iterline())

    def fetch(self, key):
        self._connection.sendall("fetch %s\n" % key)
        ret = {}
        for group, lines in self._itergraph(key):
            ret[group] = data = {}
            for line in lines:
                key, rest = line.split('.', 1)
                prop, value = rest.split(' ', 1)
                if value == 'U':
                    value = None
                else:
                    value = float(value)
                data[key] = value
        return ret

    def config(self, key):
        self._connection.sendall("config %s\n" % key)
        ret = {}
        for group, lines in self._itergraph(key):
            ret[group] = data = {}

            for line in lines:
                if line.startswith('graph_'):
                    key, value = line.split(' ', 1)
                    data[key] = value
                else:
                    key, rest = line.split('.', 1)
                    prop, value = rest.split(' ', 1)
                    if key not in data:
                        data[key] = {}
                    data[key][prop] = value
        return ret

    def nodes(self):
        self._connection.sendall("nodes\n")
        return [ line for line in self._iterline() ]

    def version(self):
        self._connection.sendall("version\n")
        return self._readline()


