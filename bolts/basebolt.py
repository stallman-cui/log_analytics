import zmq.green as zmq
import json
import logging

from configs.config import PUBTITLE, END_TOPO_SUCCESS

class BaseBolt():
    ''' handle the login log from gamelog
    '''
    def __init__(self, model, topology_context='', output_collector=''):
        self.logger = logging.getLogger('online_analytics')
        self.model = model()
        self.num = 0
        self.topicfilter = []
        self.conf = self.model.get_conf()
        self.prepare(self.conf, topology_context, output_collector)
        
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
        for sub_title in conf['sub_conf']:
            self.topicfilter.append(PUBTITLE[sub_title])
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
            self.num += 1
            body = self.model.handle(recv_tuple['body'])
            #self.logger.debug('%-30s recv_body: %s: ', self.model.__module__, body)
            if body:
                if END_TOPO_SUCCESS == body:
                    self.logger.debug('%-30s done messsage id: %d',
                                      self.model.__module__, 
                                      int(recv_tuple['id']))

                else:
                    recv_tuple['body'] = body
                    recv_tuple['state'] = self.conf['state']
                    self.send_socket.send_json(recv_tuple)
                    ack_result = self.send_socket.recv()
                    self.logger.debug('%-30s processed messsage id: %d',
                                      self.model.__module__, 
                                      int(ack_result))
            else:
                self.logger.debug('%-30s drop messsage id: %d', 
                                  self.model.__module__, 
                                  int(recv_tuple['id']))
                
    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''
