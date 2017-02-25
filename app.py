#!/usr/bin/env python3
""" Web application."""

import tornado.ioloop
import tornado.web
from tornado import websocket
from tornado import httpserver
from tornado import gen
from tornado.tcpclient import TCPClient
import os
import signal

from lamp import Lamp
import config as cfg


WS_CLIENTS = []
stream = None
lamp = Lamp()

def handle_signal(sig, frame):
    """Stop work."""
    print(sig)
    tornado.ioloop.IOLoop.instance().stop()
    if stream:
        stream.close()

class Main(tornado.web.RequestHandler):
    """Main page."""
    def get(self):
        self.render('base.html')

    def post(self):
        pass

@gen.coroutine
def parser_out(data):
    """Parser out TCP. Use lamp.parser_code."""
    next_length = lamp.parser_code(data)
    if lamp.get_value is False:
        for client in WS_CLIENTS:
            client.write_message(lamp.get_json())
    stream.read_bytes(next_length, callback=parser_out)

@gen.coroutine
def connect_to_tcpserver(host, port):
    global stream
    try: 
        stream = yield TCPClient().connect(host, port)
    except:
        handle_signal('Cannot connect to {} {}'.format(host, port), 0)
    else:
        stream.read_bytes(3, callback=parser_out)


class SocketHandler(websocket.WebSocketHandler):
    """ Handling websockets connections """
    def check_origin(self, origin):
        return True

    def open(self):
        self.set_nodelay(True)
        if self not in WS_CLIENTS:
            WS_CLIENTS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        if self in WS_CLIENTS:
            WS_CLIENTS.remove(self)

def make_app():
    return tornado.web.Application(
        [(r"/", Main),
         (r'/ws', SocketHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",)


if __name__ == "__main__":
    host = input("Host: ")
    port = input("Port: ")
    if not host:
        host = cfg.tcp_host
    if not port:
        port = cfg.tcp_port
    connect_to_tcpserver(host, port)
    print("Connect to {} {}".format(host, port))
    signal.signal(signal.SIGINT, handle_signal)
    io_loop = tornado.ioloop.IOLoop.instance()
    app = make_app()
    io_loop.http_server = httpserver.HTTPServer(app)
    io_loop.http_server.listen(cfg.http_port)
    print("Start HTTP localhost {}".format(cfg.http_port))
    io_loop.start()
    tornado.ioloop.IOLoop.instance().stop()

