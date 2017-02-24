#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from tornado import websocket
from tornado import httpserver
from tornado import gen
from tornado import httpclient
from tornado import httputil
import os
#import websocket as ws_client
import json


class BaseHandler(tornado.web.RequestHandler):
    def get_current_host_port(self):
        if self.get_secure_cookie("host") and self.get_secure_cookie("port"):
            return True

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print("MainHandler")
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("login_tornado.html")

    def post(self):
        print("AuthLoginHandle POST")
        host = self.get_argument("host", "127.0.0.1")
        port = self.get_argument("port", "9999")
        self.set_host_port(username)
        self.redirect(self.get_argument("next", "/"))

    def set_host_port(self, host, port):
        if host:
            self.set_secure_cookie("host", tornado.escape.json_encode(host))
            self.set_secure_cookie("port", tornado.escape.json_encode(port))
        else:
            self.clear_cookie("host")
            self.clear_cookie("port")

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class Main(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('base.html')

def make_app():
    return tornado.web.Application([
        (r"/", Main),
        (r"/login_tornado", AuthLoginHandler),
        ],
        template_path = os.path.join(
            os.path.dirname(__file__), "templates"),
        static_path = os.path.join(
            os.path.dirname(__file__), "static"),
        debug=True,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    login_url= "/login_tornado")


if __name__ == "__main__":
    app = make_app()
    http_server = httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
