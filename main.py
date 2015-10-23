#coding:utf8
import sys
import config
from ws_server import WebSocketServer
import log
from ws_server import WebSocketMsgHandler
from pubsub import SubscribeManager
from pubsub import Publisher
import signal
import json
from charts import ChartAgent
from datasets import DBChartAgent
from threading import Thread
import time
import datasets


class DvClinetDispatcher(WebSocketMsgHandler):
    def __init__(self, sub, dbc):
        self.sub = sub
        self.dbc = dbc
        self.on_close_cb = set()
        WebSocketMsgHandler.__init__(self)

    def on_client_open(self, client):
        WebSocketMsgHandler.on_client_open(self, client)
        log.debug('open')

    def handle_charts(self, data):
        #{u'chart_id': u'chart', u'chart_name': u'online', u'mode': u'static', limit:20, server:'2003'}
        chart_name = data['chart_name']
        limit = data['limit']
        server = data['server']
        channel = chart_name
        latest = self.dbc.getLatestISK(channel, server, limit)
        ca = ChartAgent(self, data['chart_id'], channel)
        if data['mode'] == 'static':
            ca.draw_line(channel, channel, latest)
            pass
        else:
            #dynamic data
            ca.draw_line(channel, channel, latest)
            current_value = list(latest[-1])   #time,ival,sval
            def on_recv_channel_msg(data):
                if server != data['server']:
                    return
                current_value[0] = data['time']
                if data['op'] == 'inc':
                    current_value[1] = current_value[1] + data['value']
                else:
                    current_value[1] = current_value[1] - data['value']
                ca.update(current_value)
                pass
            self.sub.subscribe(channel, on_recv_channel_msg)
            def on_close():
                self.sub.unsubscribe(channel, on_recv_channel_msg)
            self.on_close_cb.add(on_close)
            pass

    def on_client_message(self, jobj):
        if jobj['type'] == 'charts':
            self.handle_charts(jobj['data'])

    def on_client_close(self):
        log.debug('close')
        for ocb in self.on_close_cb:
            ocb()
        self.on_close_cb.clear()
        #unsubscribe

def main():
    log.init_logger(config.LOG_FILE)
    log.set_level(config.LOG_LEVEL)

    sub = SubscribeManager(config.REDIS_MQ_HOST,config.REDIS_MQ_PORT,config.REDIS_MQ_DB)
    dbc = DBChartAgent(config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWD, config.DB_NAME)
    wss = WebSocketServer(config.WSS_URI, DvClinetDispatcher(sub, dbc), host=config.WSS_HOST, port=config.WSS_PORT)

    def test_push_online():
        dbc.createKey("online")
        pub = Publisher(config.REDIS_MQ_HOST, config.REDIS_MQ_PORT, config.REDIS_MQ_DB)
        while True:
            dbc.incKey("online","2003", 2)
            pub.publish('online', {'server':'2003', "op":"inc", "value":1, "time": datasets.current_ms()})
            time.sleep(1)

    tester = Thread(target=test_push_online)
    tester.setDaemon(True)
    wss.setDaemon(True)
    wss.start()
    tester.start()

    exit_main = False
    def stop():
        log.info("stop the io thread ...")
        exit_main=True
        #wss.stop()
        #tester.stop()
    signal.signal(signal.SIGQUIT, stop)

    while not exit_main:
        sub.poll()

    wss.join()
    tester.join()


if __name__ == '__main__':
    main()
