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

def handle_signal(sig, frame):
    """Stop work."""
    print(sig)
    #io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.stop()

class Main(tornado.web.RequestHandler):
    """Main page."""
    def get(self):
        self.render('base.html')

    def post(self):
        pass

@gen.coroutine
def parser_out(stream, data, lamp):
    """Parser out TCP. Use lamp.parser_code."""
    next_length = lamp.parser_code(data)
    if lamp.get_value is False:
        for client in WS_CLIENTS:
            client.write_message(lamp.get_json())
    data = yield stream.read_bytes(next_length)
    parser_out(stream, data, lamp)

@gen.coroutine
def connect_to_tcpserver():
    lamp = Lamp()
    host = input("Host: ")
    port = input("Port: ")
    if not host:
        host = cfg.tcp_host
    if not port:
        port = cfg.tcp_port
    print("Connect to {} {}".format(host, port))
    try: 
        stream = yield TCPClient().connect(host, port)
    except:
        handle_signal('Cannot connect to {} {}'.format(host, port), 0)
    else:
        data = yield stream.read_bytes(cfg.default_length_data_tcp)
        parser_out(stream, data, lamp)


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
    signal.signal(signal.SIGINT, handle_signal)
    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.connect_to_tcpserver = connect_to_tcpserver()
    io_loop.http_server = httpserver.HTTPServer(make_app())
    io_loop.http_server.listen(cfg.http_port)
    print("Start HTTP localhost {}".format(cfg.http_port))
    io_loop.start()
    io_loop.stop()

