import zmq.green as zmq
import json

from configs.config import PUBTITLE
from bolt import Bolt

class LoginBolt(Bolt):
    ''' handle the login log from gamelog
    '''
    num = 0
    def __init__(self):
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
        self.topicfilter = PUBTITLE['login_logcount']
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
            #print('login execute: %d ' % LoginBolt.num)
            LoginBolt.num += 1
            
            try:
                area = recv_tuple['body']['area']
                plat = recv_tuple['body']['data']['corpid']
                acctid = recv_tuple['body']['data']['acct']
            except KeyError as e:
                print('message: %d KeyError: %s' % (recv_tuple['id'],str(e)))
                return
                
            recv_tuple['body'] = {
                'area' : area,
                'plat' : plat,
                'userlist' : [acctid,],
            }
            recv_tuple['state'] = "login"
            #print(json.dumps(recv_tuple, indent=3))
            self.send_socket.send(json.dumps(recv_tuple))
            ack_result = self.send_socket.recv()
            print('Login processed messsage id: %d' % int(ack_result))

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

