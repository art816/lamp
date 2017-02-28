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


class Main(tornado.web.RequestHandler):
    """Main page."""
    def get(self):
        self.render('base.html')

    def post(self):
        pass


class SocketHandler(websocket.WebSocketHandler):
    """ Handling websockets connections """
    ws_clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        self.set_nodelay(True)
        if self not in self.ws_clients:
            self.ws_clients.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        if self in self.ws_clients:
            self.ws_clients.remove(self)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", Main),
            (r'/ws', SocketHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        )
        super(Application, self).__init__(handlers, **settings)


def get_host_port():
    host = input("Host: ")
    port = input("Port: ")
    if not host:
        host = cfg.tcp_host
    if not host:
        port = cfg.tcp_port
    return host, port

@gen.coroutine
def parser_out(stream, data, lamp):
    """Parser out TCP. Use lamp.parser_code."""
    next_length = lamp.parser_code(data)
    if lamp.get_value is False:
        for client in SocketHandler.ws_clients:
            client.write_message(lamp.get_json())
    data = yield stream.read_bytes(next_length)
    parser_out(stream, data, lamp)

@gen.coroutine
def connect_to_tcpserver(host, port):
    lamp = Lamp()
    try: 
        stream = yield TCPClient().connect(host, port)
    except:
        print('Cannot connect to {} {}'.format(host, port))
        exit(0)
    else:
        print('connect to {} {}'.format(host, port))
        data = yield stream.read_bytes(cfg.default_length_data_tcp)
        parser_out(stream, data, lamp)

def make_app():
    host, port = get_host_port()
    connect_to_tcpserver(host, port)
    #print("Connect to {} {}".format(host, port))
    return Application()


if __name__ == "__main__":
    app = make_app()
    app.listen(cfg.http_port)
    print("Start HTTP localhost {}".format(cfg.http_port))
    tornado.ioloop.IOLoop.current().start()

