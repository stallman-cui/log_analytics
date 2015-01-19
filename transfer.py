#!/usr/bin/env python
import gevent
import zmq.green as zmq
from gevent.queue import Queue
import json
import sys
import logging

from configs.config import PUBTITLE
from spouts.basespout import BaseSpout
from bolts.basebolt import BaseBolt

from models.daemon import Daemon
from models.gamelogmodel import GamelogModel
from models.paymentmodel import PaymentModel
from models.signupmodel import SignupModel
from models.loginmodel import LoginModel
from models.createrolemodel import CreateroleModel
from models.payorderusermodel import PayorderUserModel
from models.servermodel import ServerModel

class Transfer(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)
        self.context = zmq.Context()
        self.messages = Queue()
        self.logger = logging.getLogger('online_analytics')

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
            #else:
            #    self.logger.debug('messages queue is empty, may be all the request id done')
            gevent.sleep(0.01)

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

    # generate a data process
    def make_bolt(self, model):
        bolt = BaseBolt(model)
        while True:
            bolt.execute()
            gevent.sleep(0.1)

    def make_spout(self, model):
        spout = BaseSpout(model)
        while True:
            spout.next_tuple()
            gevent.sleep(3600)

    def init_coroutines(self):
        coroutines = []
        coroutines.append(gevent.spawn(self.receiver))
        coroutines.append(gevent.spawn(self.sender))

        all_bolt_models = [LoginModel, SignupModel, CreateroleModel, 
                           PayorderUserModel, ServerModel,
        ]
        all_spout_models = [GamelogModel, PaymentModel,]

        for each_model in all_bolt_models:
            coroutines.append(gevent.spawn(self.make_bolt, each_model))

        for each_model in all_spout_models:
            coroutines.append(gevent.spawn(self.make_spout, each_model))

        gevent.joinall(coroutines)

    def run(self):
        self.init_coroutines()

if __name__ == "__main__":
    online_analytics = Transfer('/home/cui/log_analytics/log.pid')
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
    else:
        print('Usage: %s start|stop|restart' % sys.argv[0])
        sys.exit(2)
