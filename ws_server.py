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
        self.reply(msg)

    def on_client_close(self):
        log.debug('close')
        self.client = None

    def reply(self, mtype, data):
        jmsg = json.dumps({'type':mtype, 'data':data})
        log.debug('reply msg:'+jmsg)
        self.client.write_message(jmsg)


class WebSocketServer(Thread):
    def __init__(self, uri, dispatcher, host=None, port=8888):
        Thread.__init__(self)
        #############################################
        self.uri = uri
        self.dispatcher = dispatcher
        self.port = port
        self.host = host

        class _WebSocketServerHandlerProxy(tornado.websocket.WebSocketHandler):
            hb_msg = json.dumps({u'type': u'pong', u'data': u'-*-heart-beat-*-'})
            def open(self):
                dispatcher.on_client_open(self)
            def on_message(self, message):
                objmsg = json.loads(message)
                if objmsg['type'] == 'ping':
                    self.write_message(self.hb_msg)
                else:
                   dispatcher.on_client_message(objmsg)

            def on_close(self):
                dispatcher.on_client_close()

            def check_origin(self, origin):
                return True

        self.app = tornado.web.Application([(config.WSS_PREFIX_RGX, _WebSocketServerHandlerProxy)])
        self.app.listen(address=host, port=port)
        self.io = tornado.ioloop.IOLoop.current()

    def stop(self):
        self.io.stop()
        pass

    def run(self):
        self.io.start()

if __name__ == "__main__":
    ws = WebSocketServer('', WebSocketMsgHandler())
    ws.setDaemon(True)
    import signal
    def stop_ws():
        ws.stop()

    signal.signal(signal.SIGINT, stop_ws)
    import sys
    signal.signal(signal.SIGTERM, sys.exit)
    ws.start()
    ws.join()


