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


from parser_bytes import Parser

WS_CLIENTS = []
stream = []
parser = Parser()

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
    if parser.parse_value:
        parser.parse_value = False
        value = parser.pars_value(data, len(data))
        parser.value = value
        parsed = parser.value_to_name((parser.parsed_type, parser.length, parser.value))
        if parsed[0]:
            print(parsed)
        for client in WS_CLIENTS:
            client.write_message('data=' + data.decode('utf8'))
        stream.read_bytes(3, callback=out)
    else:
        #print('len', len(data))
        my_type, length = parser.pars_type_length(data)
        parser.parsed_type = my_type
        parser.length = length
        parser.value = ''
        #print('length=', length)
        if length:
            stream.read_bytes(length, callback=out)
            parser.parse_value = True
        else:
            parsed = parser.value_to_name((parser.parsed_type, parser.length, parser.value))
            if parsed[0]:
                print(parsed)
            for client in WS_CLIENTS:
                client.write_message('data=' + data.decode('utf8'))
            stream.read_bytes(3, callback=out)


@gen.coroutine
def connect_to_tcpserver():
    global stream
    stream = yield TCPClient().connect("localhost", 8000)
    stream.write(b'\x01\x02\x03\x04\n')
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
    app = make_app()
    app.parser = Parser()
    connect_to_tcpserver()
    http_server = httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    connect_to_tcpserver.stream.close()
    tornado.ioloop.IOLoop.current().stop()

