"""Test TCP server."""
import sys
print(sys.path)

import signal
import time
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
import os



def handle_signal(sig, frame):
    IOLoop.instance().stop()
    IOLoop.instance().server.stop()
    print("CLOSE")

class EchoServer(TCPServer):
    """Write messages."""

    def handle_stream(self, stream, address):
        self._stream = stream
        i = 0
        while True:
            #Write only commands on, off color.
            i += 1
            if self._stream:
                self._stream.write(b'\x20\x00\x03' + os.urandom(3))
                time.sleep(0.3)
                if i%2:
                    self._stream.write(b'\x12\x00\x00')
                else:
                    self._stream.write(b'\x13\x00\x00')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    io_loop = IOLoop.instance()
    io_loop.server = EchoServer()
    io_loop.server.listen(8000)
    io_loop.start()


