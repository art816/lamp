import signal
import time
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
import os



def handle_signal(sig, frame):
    IOLoop.instance().add_callback(IOLoop.instance().stop)


class EchoServer(TCPServer):

    def handle_stream(self, stream, address):
        self._stream = stream
        i = 0
        while True:
            i += 1
            if self._stream:
                self._stream.write(os.urandom(10))
    #        time.sleep(3)
        #self._read_line()


    def _read_line(self):
        self._stream.read_bytes(1, self._handle_read)

    def _handle_read(self, data):
        self._stream.write(data)
        self._read_line()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    server = EchoServer()
    server.listen(8000)
    IOLoop.instance().start()
    IOLoop.instance().close()

