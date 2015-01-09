import zmq.green as zmq
import json
import logging

from configs.config import PUBTITLE
from bolts.bolt import Bolt
from models.servermodel import ServerModel

class ServerBolt(Bolt):
    ''' Collect the login, signup, createrole, payment
    for area and plat analytics
    '''
    num = 0
    def __init__(self):
        self.prepare()
        self.logger = logging.getLogger('online_analytics')
        self.model = ServerModel()

    def prepare(self, conf='', topology_context='', output_collector=''):
        ''' Called when a task for this component is Initialized
        within a worker on the cluster.
            conf: The configuration for this spout.
            topology_context: The input and output information.
            output_collector: The collector is used to emit tuples
            from this spout.
        '''
        self.context = zmq.Context()
        self.recv_socket = self.context.socket(zmq.SUB)
        self.recv_socket.connect("tcp://127.0.0.1:5001")
        self.topicfilter = [PUBTITLE['login'], PUBTITLE['signup'], PUBTITLE['createrole']]
        for top in self.topicfilter:
            self.recv_socket.setsockopt(zmq.SUBSCRIBE, top)

        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.connect("tcp://127.0.0.1:5000")


    def execute(self):
        ''' Process a single tuple of input. '''
        input = self.recv_socket.recv()
        if input:
            #topic = input[0:4]
            recv_tuple = input[4:]
            recv_tuple = json.loads(recv_tuple)
            #logging.debug('server execute: %d ', ServerBolt.num)
            ServerBolt.num += 1
            
            body = self.model.handle(recv_tuple['body'])
            recv_tuple['state'] = "server"
            recv_tuple['body'] = body

            self.send_socket.send_json(recv_tuple)
            ack_result = self.send_socket.recv()
            self.logger.debug('%-10s processed messsage id:  %d', 'Server', int(ack_result))

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

