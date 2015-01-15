import zmq.green as zmq
import logging
from spouts.spout import Spout

class BaseSpout(Spout):
    """ read the payment data,
    and send it
    """
    MAX = 999999
    message_id = 0

    def __init__(self, model, topology_context='', output_collector=''):
        self.logger = logging.getLogger('online_analytics')
        self.open()
        self.model = model()
        self.conf = self.model.get_conf()

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
        self.logger.info('%-10s Starting read ... ', self.model.__module__)
        all_data = self.model.get_data()
        for line in all_data:
            message_tuple = {
                'id' : BaseSpout.message_id % BaseSpout.MAX,
                'body' : line,
                'state' : self.conf['state']
            }
            BaseSpout.message_id += 1
            self.socket.send_json(message_tuple)
            ack_no = self.socket.recv_string()
            if ack_no == str(message_tuple['id']):
                self.ack(ack_no)
            else:
                self.fail(ack_no)
        self.logger.info('%-10s End the read ...', self.model.__module__)

    def ack(self, msg_id):
        ''' The tuple emiited by this spout with the msg_id has been fully processed. '''
        #print("Gamelog: request was Sucessed, messsage_id: %d \n" % int(msg_id))

    def fail(self, msg_id):
        ''' The tuple emitted by this spout with the msg_id has filed to be fully processed. '''
        self.logger.error('%-20s emiited message id %d failed.', self.model.__module__, int(msg_id))

        print("Gamelog: request was Failed, messsage_id: %d \n" % int(msg_id))





