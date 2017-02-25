#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from tornado import websocket
from tornado import httpserver
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado.tcpclient import TCPClient
import os
#import websocket as ws_client
import json
import signal

from parser_bytes import Parser
from lamp import Lamp

WS_CLIENTS = []
stream = []
lamp = Lamp()
parser = Parser()

def handle_signal(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback(
        tornado.ioloop.IOLoop.instance().stop)
    print("CLOSE")

class Main(tornado.web.RequestHandler):
    def get(self):
        self.render('base.html')


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

def out(data):
    data = data
    next_length = lamp.parser_code(data)
    if lamp._get_value is False:
        for client in WS_CLIENTS:
            client.write_message(lamp._get_json())
    stream.read_bytes(next_length, callback=out)

@gen.coroutine
def connect_to_tcpserver():
    global stream
    stream = yield TCPClient().connect("localhost", 8000)
    stream.read_bytes(3, callback=out)


def make_app():
    return tornado.web.Application([
        (r"/", Main),
        (r'/ws', SocketHandler),
        ],
        template_path = os.path.join(
            os.path.dirname(__file__), "templates"),
        static_path = os.path.join(
            os.path.dirname(__file__), "static"),
        debug=True,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    app = make_app()
    app.parser = Parser()
    connect_to_tcpserver()
    http_server = httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    tornado.ioloop.IOLoop.instance().stop()
    tornado.ioloop.IOLoop.instance().close()

