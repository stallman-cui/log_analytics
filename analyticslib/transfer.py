#!/usr/bin/env python
import json
import logging
import gevent
import zmq.green as zmq
from gevent.queue import Queue

from configs.config import PUBTITLE
from configs.config import send_addr, receive_addr

class Transfer():
    MAX = 999999
    message_id = 0

    def __init__(self):
        ####Daemon.__init__(self, pidfile)
        self.context = zmq.Context()
        self.messages = Queue()
        self.logger = logging.getLogger('online_analytics')

    # Publish all the messages
    def sender(self):
        send_socket = self.context.socket(zmq.PUB)
        send_socket.setsockopt(zmq.SNDHWM, 50000)
        send_socket.bind(send_addr)
        while True:
            if not self.messages.empty():
                message_tuple = self.messages.get_nowait()
                topic = PUBTITLE[message_tuple['state']]
                send_socket.send("%s %s" % (topic, json.dumps(message_tuple)))
                gevent.sleep(0.005)
            else:
                gevent.sleep(1)
                #self.logger.info('messages queue is empty, may be all the request is done or not start')
            gevent.sleep(0)

    # Collect all the messages        
    def receiver(self):
        server_socket = self.context.socket(zmq.REP)
        server_socket.bind(receive_addr)
        while True:
            message_tuple = server_socket.recv_json()
            if not message_tuple.get('id', 0):
                Transfer.message_id += 1
                message_tuple = {
                    'id' : Transfer.message_id % Transfer.MAX,
                    'body' : message_tuple['body'],
                    'state' : message_tuple['state']
                }
                
            self.messages.put_nowait(message_tuple)
            server_socket.send(str(message_tuple['id']))
