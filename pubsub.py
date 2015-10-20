
import redis
import log
from threading import Thread

class SubscribeManager:
    pass
    def __init__(self, host, port, dbid):
        self.listenner = {}
        rc = redis.Redis(host,port,dbid)
        self.ps = rc.pubsub()
        self.lock = Thread.Lock()
        pass

    def subscribe(self, channel, cb):
        with self.lock:
            if self.listenner.has_key(channel):
                self.listenner[channel].put(cb)
            else:
                self.listenner[channel] = [cb]

            self.ps.subscribe([channel])

    def unsubscribe(self, channel, cb):
        with self.lock:
            self.listenner[channel].pop(cb)
            if len(self.listenner[channel] == 0):
                self.ps.unsubscribe(channel)

    def poll(self):
        #get msg
        for item in self.ps.listen():
            if item['type'] == 'message':
                channel = item['channel']
                data = item['data']
                log.debug("recv msg data")
                with self.lock:
                    if self.listenner.has_key(channel):
                        for cb in self.listenner[channel]:
                            cb(data)


class Publisher:
    def __init__(self, host, port, dbid):
        selfrc = redis.Redis(host,port,dbid)
        pass

    def publish(self, channel, msg):
        self.rc.publish(channel, msg)


