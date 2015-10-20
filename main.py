#coding:utf8
import sys
import config
from ws_server import WebSocketServer
import log
from ws_server import WebSocketMsgHandler
from pubsub import SubscribeManager
import signal

class DvClinetDispatcher(WebSocketMsgHandler):
    def __init__(self, sub):
        self.sub = sub
        WebSocketMsgHandler.__init__(self)

    def on_client_open(self):
        log.debug('open')

    def on_client_message(self, msg):
        log.debug('msg:'+msg)

    def on_client_close(self):
        log.debug('close')

def main():
    log.init_logger(config.LOG_FILE)
    log.set_level(config.LOG_LEVEL)

    sub = SubscribeManager(config.REDIS_MQ_HOST,config.REDIS_MQ_PORT,config.REDIS_MQ_DB)
    wss = WebSocketServer(config.WSS_URI, DvClinetDispatcher(sub), host=config.WSS_HOST, port=config.WSS_PORT)

    wss.start()

    def stop():
        wss.stop()
    signal.signal(signal.SIGQUIT, stop)
    wss.join()

if __name__ == '__main__':
    main()
