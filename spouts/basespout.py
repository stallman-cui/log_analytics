import zmq.green as zmq
import logging

class BaseSpout():
    """ read the data, and send it
    """
    def __init__(self, model, topology_context='', output_collector=''):
        self.logger = logging.getLogger('online_analytics')
        self.model = model()
        self.conf = self.model.get_conf()
        self.count = 0
        self.open()

    def open(self, conf='', topology_context='', output_collector=''):
        ''' Called when a task for this component is initialized '''
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5000")

    def close(self):
        ''' Called when an spout is going to be shutdown. '''

    def activate(self):
        ''' Called when a spout has been activated out of a deactivated mode. '''
        
    def deactivate(self):
        ''' Called when a spout has been deactivated'''
        
    def next_tuple(self):
        ''' When this method is called, the spout emit 
        tuples to the output collector. 
        '''

    def ack(self, msg_id):
        ''' The tuple emiited by this spout with the msg_id has been fully processed. '''

    def fail(self, msg_id):
        ''' The tuple emitted by this spout with the msg_id has filed to be fully processed. '''
