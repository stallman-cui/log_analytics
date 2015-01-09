import zmq.green as zmq
import json
import logging

from configs.config import PUBTITLE
from bolts.bolt import Bolt
from lib import get_ts

class CreateroleBolt(Bolt):
    ''' handle the login log from gamelog
    '''
    num = 0
    def __init__(self):
        self.logger = logging.getLogger('online_analytics')
        self.prepare()

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
        self.topicfilter = PUBTITLE['createrole_logcount']
        self.recv_socket.setsockopt(zmq.SUBSCRIBE, self.topicfilter)

        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.connect("tcp://127.0.0.1:5000")

    def execute(self):
        ''' Process a single tuple of input. '''

        input = self.recv_socket.recv()
        if input:
            #topic = input[0:4]
            recv_tuple = input[4:]
            recv_tuple = json.loads(recv_tuple)
            #logging.debug('createrole execute: %d ', CreateroleBolt.num)
            CreateroleBolt.num += 1
            
            try:
                area = recv_tuple['body']['area']
                plat = recv_tuple['body']['data']['corpid']
                acctid = recv_tuple['body']['data']['acct']
            except KeyError as e:
                self.logger.error('message: %d KeyError: %s', recv_tuple['id'], str(e))
                return
                
            recv_tuple['body'] = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(),
                'user' : acctid
            }
            recv_tuple['state'] = "createrole"
            #print(json.dumps(recv_tuple, indent=3))
            self.send_socket.send_json(recv_tuple)
            ack_result = self.send_socket.recv()
            self.logger.debug('%-10s processed messsage id:  %d', 'Createrole', int(ack_result))

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

