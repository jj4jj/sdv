#coding:utf8
import sys
import config
from ws_server import WebSocketServer
import log
from ws_server import WebSocketMsgHandler
from pubsub import SubscribeManager
import signal
import json
from charts import ChartAgent
from datasets import DBChartAgent



class DvClinetDispatcher(WebSocketMsgHandler):
    def __init__(self, sub, dbc):
        self.sub = sub
        self.dbc = dbc
        WebSocketMsgHandler.__init__(self)

    def on_client_open(self, client):
        WebSocketMsgHandler.on_client_open(self, client)
        log.debug('open')

    def handle_charts(self, data):
        #{u'chart_id': u'chart', u'chart_name': u'online', u'mode': u'static', limit:20, server:'2003'}
        ca = ChartAgent(self, data['chart_id'])
        channel = data['chart_name']
        limit = data['limit']
        server = data['server'];
        if data['mode'] == 'static':
            latest = self.dbc.getLatestISK(channel, server, limit)
            ca.draw_line(channel, channel, latest)
            pass
        else:
            pass

    def on_client_message(self, msg):
        jobj = json.loads(msg)  #{u'type': u'charts', u'data': {u'chart_id': u'chart', u'type': u'line', u'mode': u'static'}}
        log.debug("recv:" + str(jobj))
        #if is a chart send to chart handler
        #self.sub.subscribe('line'
        if jobj['type'] == 'charts':
            self.handle_charts(jobj['data'])

    def on_client_close(self):
        log.debug('close')
        #unsubscribe

def main():
    log.init_logger(config.LOG_FILE)
    log.set_level(config.LOG_LEVEL)


    sub = SubscribeManager(config.REDIS_MQ_HOST,config.REDIS_MQ_PORT,config.REDIS_MQ_DB)
    dbc = DBChartAgent(config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWD, config.DB_NAME)
    wss = WebSocketServer(config.WSS_URI, DvClinetDispatcher(sub, dbc), host=config.WSS_HOST, port=config.WSS_PORT)

    wss.start()

    def stop():
        log.info("stop the io thread ...")
        wss.stop()
    signal.signal(signal.SIGQUIT, stop)
    wss.join()
    while True:
        sub.poll()

if __name__ == '__main__':
    main()
