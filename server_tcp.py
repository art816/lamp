import signal
import time
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
import os



def handle_signal(sig, frame):
    IOLoop.instance().add_callback(IOLoop.instance().stop)
    print("CLOSE")

class EchoServer(TCPServer):

    def handle_stream(self, stream, address):
        self._stream = stream
        i = 0
        while True:
            i += 1
            if self._stream:
                self._stream.write(b'\x20\x00\x03' + os.urandom(3))
                time.sleep(0.3)
                if i%2:
                    self._stream.write(b'\x12\x00\x00')
                else:
                    self._stream.write(b'\x13\x00\x00')
                    
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
    print("CLOSE2")


