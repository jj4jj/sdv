
import redis
import log
from threading import Thread
import threading
import json

class SubscribeManager:
    pass
    def __init__(self, host, port, dbid):
        self.listenner = {}
        rc = redis.Redis(host,port,dbid)
        self.ps = rc.pubsub()
        self.lock = threading.Lock()
        pass

    def subscribe(self, channel, cb):
        with self.lock:
            if self.listenner.has_key(channel):
                self.listenner[channel].add(cb)
            else:
                self.listenner[channel] = set([cb])

            self.ps.subscribe([channel])

    def unsubscribe(self, channel, cb):
        with self.lock:
            self.listenner[channel].remove(cb)
            if len(self.listenner[channel]) == 0:
                self.ps.unsubscribe(channel)

    def poll(self):
        #get msg
        for item in self.ps.listen():
            if item['type'] == 'message':
                channel = item['channel']
                data = item['data']
                with self.lock:
                    if self.listenner.has_key(channel):
                        for cb in self.listenner[channel]:
                            jdic = json.loads(data)
                            cb(jdic)


class Publisher:
    def __init__(self, host, port, dbid):
        self.rc = redis.Redis(host,port,dbid)
        pass

    def publish(self, channel, ojmsg):
        jmsg = json.dumps(ojmsg)
        self.rc.publish(channel, jmsg)


