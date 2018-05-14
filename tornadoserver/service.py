# -*-coding: utf-8 -*-
# __author__ : tinytiger
# __time__   : '2018/1/4 11:07'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options

from tornadoserver.app import handler

define("port", default=8000, help="run on the given port", type=int)

Handlers = [(r"/trans", handler.Translate)]

application = Application(
    Handlers
)

if __name__ == '__main__':
    server = HTTPServer(application)
    server.listen(options.port)

    ioloop = IOLoop.current()
    ioloop.start()
