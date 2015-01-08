#!/usr/bin/env python
import gevent
import zmq.green as zmq
import json
from gevent.queue import Queue

from configs.config import PUBTITLE
from spouts.gamelogspout import GamelogSpout
from bolts.loginbolt import LoginBolt
from bolts.serverbolt import ServerBolt
from bolts.signupbolt import SignupBolt

login = LoginBolt()
server = ServerBolt()
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
                #print(message_tuple['body']['op']['code'])
                try:
                    topic = PUBTITLE[message_tuple['body']['op']['code']]
                except:
                    #print('Sender: we do not care: %s' % str(e))
                    continue
            else:
                topic = PUBTITLE[message_tuple['state']]
            send_socket.send("%s %s" % (topic, json.dumps(message_tuple)))

        gevent.sleep(0.01)

# Receive the messages        
def receiver():
    server_socket = context.socket(zmq.REP)
    server_socket.bind("tcp://127.0.0.1:5000")
    global messages

    while True:
        message_tuple = server_socket.recv()
        if message_tuple:
            message_tuple = json.loads(message_tuple)
            #if not messages.full():
            messages.put_nowait(message_tuple)
            #print('Receiver: put-messages size: %d' % messages.qsize())
            #print("Receiver: received the request: messsage_id: %d " % message_tuple['id'])
            server_socket.send(str(message_tuple['id']))
        else:
            server_socket.send('Error')

# generate a data source
def make_spout(spoutclass=GamelogSpout):
    spout = spoutclass()
    while True:
        spout.next_tuple()
        gevent.sleep(20)

# generate a data process
def make_bolt(boltclass):
    bolt = boltclass()
    while True:
        bolt.execute()
        gevent.sleep(0.1)

coroutines = []
coroutines.append(gevent.spawn(receiver))
coroutines.append(gevent.spawn(sender))

all_bolts = [LoginBolt, ServerBolt, SignupBolt,]
all_spouts = [GamelogSpout,]

for each_bolt in all_bolts:
    coroutines.append(gevent.spawn(make_bolt, each_bolt))

for each_spout in all_spouts:
    coroutines.append(gevent.spawn(make_spout, each_spout))

gevent.joinall(coroutines)
