#!/usr/bin/env python
import sys
import json
import logging
import os
import time
import multiprocessing
import gevent
import zmq.green as zmq
from gevent.queue import Queue

basedir, bin = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.insert(0, basedir)

from models.daemon import Daemon
from worker import Worker
from configs.config import PUBTITLE
from bolts.basebolt import BaseBolt
from spouts.basespout import BaseSpout
from allmodel import all_bolt_models
from allmodel import all_spout_models

####class Transfer(Daemon):
class Transfer():
    def __init__(self, pidfile):
        ####Daemon.__init__(self, pidfile)
        self.context = zmq.Context()
        self.messages = Queue()
        self.logger = logging.getLogger('online_analytics')
        self.pidfile = pidfile

    # Publish all the messages
    def sender(self):
        send_socket = self.context.socket(zmq.PUB)
        send_socket.bind("tcp://127.0.0.1:5001")
        while True:
            if not self.messages.empty():
                message_tuple = self.messages.get_nowait()
                if message_tuple['state'] == 'gamelog':
                    try:
                        topic = PUBTITLE[message_tuple['body']['op']['code']]
                    except:
                        continue
                else:
                    topic = PUBTITLE[message_tuple['state']]
                send_socket.send("%s %s" % (topic, json.dumps(message_tuple)))
            else:
                gevent.sleep(1)
                #self.logger.info('messages queue is empty, may be all the request is done or not start')
            gevent.sleep(0)

    # Collect all the messages        
    def receiver(self):
        server_socket = self.context.socket(zmq.REP)
        server_socket.bind("tcp://127.0.0.1:5000")
        while True:
            message_tuple = server_socket.recv_json()
            if message_tuple:
                self.messages.put_nowait(message_tuple)
                server_socket.send(str(message_tuple['id']))
            else:
                server_socket.send_string('Error')
    
    def update_status(self):
        pid = int(file(self.pidfile).read().strip())
        worker = Worker()
        while True:
            worker.update(pid, int(time.time()))
            gevent.sleep(1)

    # generate a data process
    def make_bolt(self, model):
        bolt = BaseBolt(model)
        while True:
            bolt.execute()
            gevent.sleep(0)

    def make_spout(self, model):
        spout = BaseSpout(model)
        while True:
            spout.next_tuple()
            gevent.sleep(60)

    def init_base(self):
        thread = []
        thread.append(gevent.spawn(self.receiver))
        thread.append(gevent.spawn(self.sender))
        thread.append(gevent.spawn(self.update_status))
        gevent.joinall(thread)

    def init_spout(self):
        coroutines = []
        for each_model in all_spout_models:
            coroutines.append(gevent.spawn(self.make_spout, each_model))
        gevent.joinall(coroutines)
        
    def init_bolt(self):
        coroutines = []
        for each_model in all_bolt_models:
            coroutines.append(gevent.spawn(self.make_bolt, each_model))
        gevent.joinall(coroutines)

    def run(self):
        base_process = multiprocessing.Process(name='base_thread', target=self.init_base)
        bolt_process = multiprocessing.Process(name='bolt', target=self.init_bolt)
        spout_process = multiprocessing.Process(name='spout', target=self.init_spout)
        
        base_process.start()
        bolt_process.start()
        spout_process.start()

if __name__ == "__main__":
    online_analytics = Transfer('/home/cui/log_analytics/log.pid')
    online_analytics.run()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            online_analytics.start()
        elif 'stop' == sys.argv[1]:
            online_analytics.stop()
        elif 'restart' == sys.argv[1]:
            online_analytics.restart()
        else:
            print('Unknown command')
            sys.exit(2)
    #else:
    #    print('Usage: %s start|stop|restart' % sys.argv[0])
    #    sys.exit(2)
