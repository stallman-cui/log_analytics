import zmq.green as zmq
import json

from lib import PUBTITLE
from bolt import Bolt

class ServerBolt(Bolt):
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
            #print('server execute: %d ' % ServerBolt.num)
            ServerBolt.num += 1
            
            try:
                area = recv_tuple['body']['area']
                plat = recv_tuple['body']['plat']
            except KeyError as e:
               print('message: %d KeyError: %s' % (recv_tuple['id'],str(e)))
               return

            body = {
                'area' : area,
                'plat' : plat,
            }
            if recv_tuple['state'] == 'login':
                body['login_userlist'] = recv_tuple['body']['userlist']

            if recv_tuple['state'] == 'signup':
                body['signup_userlist'] = recv_tuple['body']['userlist']

            if recv_tuple['state'] == 'create_role':
                body['createrole_userlist'] = recv_tuple['body']['userlist']

            recv_tuple['state'] = "server"
            recv_tuple['body'] = body
            #print(json.dumps(recv_tuple, indent=3))
            self.send_socket.send(json.dumps(recv_tuple))
            ack_result = self.send_socket.recv()
            print('Server processed messsage id: %d' % int(ack_result))

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

