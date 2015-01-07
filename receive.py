#!/usr/bin/env python
import gevent
import zmq.green as zmq
import json
from gevent.queue import Queue

from gamelogspout import GamelogSpout
from loginbolt import LoginBolt

login = LoginBolt()

context = zmq.Context()
messages = Queue()

def dispatch():
    global messages
    while True:
        if not messages.empty():
            print('get-messages size: %d' % messages.qsize())
            message_tuple = messages.get_nowait()
            if message_tuple:
                #print message_tuple
                op_code = message_tuple['body']['op']['code']
                if op_code == 'login_logcount':
                    result_tuple = login.execute(message_tuple)
                    print(result_tuple)
                    #messages.put_nowait(result_tuple)

        gevent.sleep(0.001)
                

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
            print('put-messages size: %d' % messages.qsize())
            print("Server handled the request: %d " % message_tuple['id'])
            server_socket.send(str(message_tuple['id']))
        else:
            server_socket.send('Error')

def make_spout(spout = GamelogSpout):
    gamelog_spout = spout()
    while True:
        gamelog_spout.next_tuple()
        gevent.sleep(30)

gevent.joinall([
    gevent.spawn(dispatch),
    gevent.spawn(receiver),
    gevent.spawn(make_spout(GamelogSpout)),
])
