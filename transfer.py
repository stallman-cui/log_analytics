#!/usr/bin/env python
import gevent
import zmq.green as zmq
from gevent.queue import Queue
import json

from configs.config import PUBTITLE
from spouts.basespout import BaseSpout
from bolts.basebolt import BaseBolt

from models.signupmodel import SignupModel
from models.loginmodel import LoginModel
from models.createrolemodel import CreateroleModel
from models.payorderusermodel import PayorderUserModel
from models.servermodel import ServerModel

from models.gamelogmodel import GamelogModel
from models.paymentmodel import PaymentModel

context = zmq.Context()
messages = Queue()

# Publish the messages
def sender():
    send_socket = context.socket(zmq.PUB)
    send_socket.bind("tcp://127.0.0.1:5001")
    global messages
    while True:
        if not messages.empty():
            message_tuple = messages.get_nowait()
            #print('Sender: send the message_id: %d' % message_tuple['id'])
            if message_tuple['state'] == 'gamelog':
                try:
                    topic = PUBTITLE[message_tuple['body']['op']['code']]
                except:
                    continue
            else:
                topic = PUBTITLE[message_tuple['state']]
            send_socket.send("%s %s" % (topic, json.dumps(message_tuple)))
        #else:
        #    print('message queue: ', time.time(),  messages.qsize())

        gevent.sleep(0.01)

# Receive the messages        
def receiver():
    server_socket = context.socket(zmq.REP)
    server_socket.bind("tcp://127.0.0.1:5000")
    global messages
    while True:
        message_tuple = server_socket.recv_json()
        if message_tuple:
            messages.put_nowait(message_tuple)
            server_socket.send(str(message_tuple['id']))
        else:
            server_socket.send_string('Error')

# generate a data process
def make_bolt(model):
    bolt = BaseBolt(model)
    while True:
        bolt.execute()
        gevent.sleep(0.1)

def make_spout(model):
    spout = BaseSpout(model)
    while True:
        spout.next_tuple()
        gevent.sleep(3600)

coroutines = []
coroutines.append(gevent.spawn(receiver))
coroutines.append(gevent.spawn(sender))

all_bolt_models = [LoginModel, SignupModel, CreateroleModel, 
                   PayorderUserModel, ServerModel,
]
all_spout_models = [GamelogModel, PaymentModel,]

for each_model in all_bolt_models:
    coroutines.append(gevent.spawn(make_bolt, each_model))

for each_model in all_spout_models:
    coroutines.append(gevent.spawn(make_spout, each_model))

gevent.joinall(coroutines)
