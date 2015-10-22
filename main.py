#coding:utf8
import sys
import config
from ws_server import WebSocketServer
import log
from ws_server import WebSocketMsgHandler
from pubsub import SubscribeManager
import signal
import json

class ChartAgent:
    def __init__(self, client, data):
        #{u'chart_id': u'chart', u'type': u'line', u'mode': u'static'}
        self.client = client
        self.chart_id = data.chart_id
        self.mode = data.mode
        self.type = data.type

    def __call__(self, data):
        #data->[k:v], update .
        self.update()
        pass

    def update(self):
        """
                jobj = {'type': 'render', 'data': {'chart_id': self.chart_id,\
                                                   'chart':{'xAxis':[],\
                                                            'yAxis':[],\
                                                            'legends':[],\
                                                            'series':[]}}}

        """


    def render(self):
        """
                echarts_init(area, data.chart.xAxis,
                                                    data.chart.yAxis,
                                                    data.chart.legends,
                                                    data.chart.series);
        """
        #type:render;data={chart_id:,chart:{xAxis;[],yAxis,legends,series}}
        jobj = {'type': 'render',
                'data': {'chart_id': self.chart_id,
                           'chart':{'xAxis':[],
                                    'yAxis':[],
                                    'legends':[],
                                    'series':[]}}}
        self.client.reply(json.dumps(jobj))
        pass


class DvClinetDispatcher(WebSocketMsgHandler):
    def __init__(self, sub):
        self.sub = sub
        WebSocketMsgHandler.__init__(self)

    def on_client_open(self, client):
        WebSocketMsgHandler.on_client_open(self, client)
        log.debug('open')

    def handle_charts(self, data):
        #{u'chart_id': u'chart', u'type': u'line', u'mode': u'static'}
        if data.mode == 'static':
            ChartAgent(self.client, data).render()
        else:
            pass
        pass

    def on_client_message(self, msg):
        jobj = json.loads(msg)  #{u'type': u'charts', u'data': {u'chart_id': u'chart', u'type': u'line', u'mode': u'static'}}
        log.debug("recv:" + str(jobj))
        #if is a chart send to chart handler
        #self.sub.subscribe('line'
        if jobj.type == 'charts':
            self.handle_charts(jobj.data)

    def on_client_close(self):
        log.debug('close')
        #unsubscribe

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
    while True:
        sub.poll()

if __name__ == '__main__':
    main()
