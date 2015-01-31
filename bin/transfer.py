#!/usr/bin/env python
import json
import logging
import gevent
import zmq.green as zmq
from gevent.queue import Queue

from configs.config import PUBTITLE

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
                Transfer.message_id += 1
                message = {
                    'id' : Transfer.message_id % Transfer.MAX,
                    'body' : message_tuple['body'],
                    'state' : message_tuple['state']
                }
                self.messages.put_nowait(message)
                server_socket.send(str(message['id']))
            else:
                server_socket.send_string('Error')
