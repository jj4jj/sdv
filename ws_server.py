#-*-coding:utf8-*-

from threading import Thread
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import log
import config
try:
    # py2
    from urllib.parse import urlparse
except ImportError:
    # py3
    from urlparse import urlparse


class WebSocketMsgHandler():
    def __init__(self):
        self.client = None
        pass

    def on_client_open(self, client):
        self.client = client
        log.debug('open')

    def on_client_message(self, msg):
        log.debug('msg:'+msg)
        self.write_message("echo:"+msg)

    def on_client_close(self):
        log.debug('close')
        self.client = None


class WebSocketServer(Thread):
    def __init__(self, uri, um, host, port=8888):
        Thread.__init__(self)
        #############################################
        self.uri = uri
        self.um = um
        self.port = port
        self.host = host

        class _WebSocketServerHandlerProxy(tornado.websocket.WebSocketHandler):
            def open(self):
                um.on_client_open(self)

            def on_message(self, message):
                um.on_client_message(message)

            def on_close(self):
                um.on_client_close()

            def check_origin(self, origin):
                return True

        self.app = tornado.web.Application([(config.WSS_PREFIX_RGX, _WebSocketServerHandlerProxy)])
        self.app.listen(address=host, port=port)
        self.io = tornado.ioloop.IOLoop.current()

    def stop(self):
        pass

    def run(self):
        self.io.start()

if __name__ == "__main__":
    ws = WebSocketServer('', WebSocketMsgHandler())
    ws.start()
    ws.join()

