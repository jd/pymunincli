import unittest

import SocketServer
import threading
from munin.client import Client, ClientError

class MockServer(SocketServer.TCPServer):
    allow_reuse_address = True

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
        with self.assertRaises(ClientError):
            c.connect()

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

if __name__ == "__main__":
    unittest.main()
