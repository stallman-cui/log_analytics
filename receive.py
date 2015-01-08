#!/usr/bin/env python
import gevent
import zmq.green as zmq
import json
from gevent.queue import Queue

from lib import PUBTITLE
from gamelogspout import GamelogSpout
from loginbolt import LoginBolt
from serverbolt import ServerBolt
from signupbolt import SignupBolt

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
            print('Sender: send the message_id: %d' % message_tuple['id'])
            topic = PUBTITLE[message_tuple['state']]
            send_socket.send("%s %s" % (topic, json.dumps(message_tuple)))

        gevent.sleep(0)

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
            print("Receiver: received the request: messsage_id: %d " % message_tuple['id'])
            server_socket.send(str(message_tuple['id']))
        else:
            server_socket.send('Error')

def make_spout(spoutclass=GamelogSpout):
    spout = spoutclass()
    while True:
        spout.next_tuple()
        gevent.sleep(3600)

def make_bolt(boltclass):
    bolt = boltclass()
    while True:
        bolt.execute()
        gevent.sleep(0)

gevent.joinall([
    gevent.spawn(receiver),
    gevent.spawn(sender),
    gevent.spawn(make_spout, GamelogSpout),
    gevent.spawn(make_bolt, LoginBolt),
    gevent.spawn(make_bolt, ServerBolt),
    gevent.spawn(make_bolt, SignupBolt),
])
