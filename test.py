import unittest

import SocketServer
import threading
from munin.client import Client, ClientError, _itergraph

class MockServer(SocketServer.TCPServer):
    allow_reuse_address = True

class TestIterGraph(unittest.TestCase):
    def test_none(self):

        inp = ["1", "2"]

        for graph, lines in _itergraph("foo", inp):
            self.assertEqual(graph, "foo")
            self.assertEqual(["1", "2"], list(lines))

    def test_two(self):

        inp = ["multigraph foo_1", "1", "2", "multigraph foo_2", "3", "4"]

        for graph, lines in _itergraph("foo", inp):

            if graph == "foo_1":
                self.assertEqual(["1", "2"], list(lines))
            elif graph == "foo_2":
                self.assertEqual(["3", "4"], list(lines))
            else:
                self.fail()

class TestClient(unittest.TestCase):
    def setUp(self):
        self.s = None

    def tearDown(self):
        if self.s is not None:
            self.s.shutdown()
            self.s.server_close()
            self.t.join()

    def _mock(self, handler):
        self.s = MockServer(("localhost", 9998), handler)
        self.t = threading.Thread(target=self.s.serve_forever)
        self.t.start()

    def test_denied(self):
        # Munin node just closes connection if source address is not
        # allowed access.

        class MockDeniedHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                self.request.close()

        self._mock(MockDeniedHandler)

        c = Client('localhost', port=9998)
        self.assertRaises(ClientError, c.connect)

    def test_list(self):
        class MockListHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                f = self.request.makefile()

                self.request.sendall("mock\n")
                f.readline()
                self.request.sendall("cap multigraph\n")
                f.readline()
                self.request.sendall("foo bar\n")

        self._mock(MockListHandler)

        c = Client('localhost', port=9998)
        c.connect()

        self.assertEqual(c.list(), ['foo', 'bar'])

    def test_fetch_multigraph(self):
        class MockFetchHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                f = self.request.makefile()

                self.request.sendall("mock\n")
                f.readline()
                self.request.sendall("cap multigraph\n")
                f.readline()
                self.request.sendall("multigraph foo_1\n")
                self.request.sendall("x.value 1\n")
                self.request.sendall("multigraph foo_2\n")
                self.request.sendall("y.value 2\n")
                self.request.sendall(".\n")

        self._mock(MockFetchHandler)

        c = Client('localhost', port=9998)
        c.connect()

        self.assertEqual(c.fetch("foo"), {'foo_1': {'x': 1.0}, 'foo_2': {'y': 2.0}})

    def test_fetch(self):
        class MockFetchHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                f = self.request.makefile()

                self.request.sendall("mock\n")
                f.readline()
                self.request.sendall("cap multigraph\n")
                f.readline()
                self.request.sendall("x.value 1\n")
                self.request.sendall(".\n")

        self._mock(MockFetchHandler)

        c = Client('localhost', port=9998)
        c.connect()

        self.assertEqual(c.fetch("foo"), {'foo': {'x': 1.0}})

    def test_config(self):
        class MockConfigHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                f = self.request.makefile()

                self.request.sendall("mock\n")
                f.readline()
                self.request.sendall("cap multigraph\n")
                f.readline()
                self.request.sendall("graph_info foo\n")
                self.request.sendall("x.info bar\n")
                self.request.sendall(".\n")

        self._mock(MockConfigHandler)

        c = Client('localhost', port=9998)
        c.connect()

        self.assertEqual(c.config("foo"), {'foo': {'graph_info': 'foo', 'x': {'info': 'bar'}}})

if __name__ == "__main__":
    unittest.main()
