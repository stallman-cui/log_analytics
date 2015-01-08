from spout import Spout
import zmq.green as zmq
import json

from lib import gamelog_parse

class GamelogSpout(Spout):
    """ read the gamelog data,
    and send it
    """
    MAX = 999999
    message_id = 0

    def __init__(self):
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
        #with open('/home/cui/gamelog.txt', 'r') as f:
        with open('gamelog_20150108.txt', 'r') as f:
            for line in f:
                line = gamelog_parse(line)
                if line:
                    message_tuple = {
                        'id' : GamelogSpout.message_id % GamelogSpout.MAX,
                        'body' : line,
                        'state' : "gamelog"
                    }
                    GamelogSpout.message_id += 1
                    #print message_tuple
                    self.socket.send(json.dumps(message_tuple))
                    ack_no = self.socket.recv()
                    if ack_no == str(message_tuple['id']):
                        self.ack(ack_no)
                    else:
                        self.fail(ack_no)
        
        
    def ack(self, msg_id):
        ''' The tuple emiited by this spout with the msg_id has been fully processed. '''
        print("Gamelog: request was Sucessed, messsage_id: %d \n" % int(msg_id))

    def fail(self, msg_id):
        ''' The tuple emitted by this spout with the msg_id has filed to be fully processed. '''

        print("Gamelog: request was Failed, messsage_id: %d \n" % int(msg_id))
