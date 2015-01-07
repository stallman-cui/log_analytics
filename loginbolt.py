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

    def execute(self, input):
        ''' Process a single tuple of input. '''

        if input:
            recv_tuple = input
            recv_tuple['state'] = "login"
            print('login execute: %d ' % LoginBolt.num)
            #print recv_tuple
            LoginBolt.num += 1
            
            try:
                area = recv_tuple['body']['area']
                plat = recv_tuple['body']['data']['corpid']
                acctid = recv_tuple['body']['data']['acct']
            except KeyError as e:
                print('KeyError: %s' % str(e))

            recv_tuple['body'] = {
                'area' : area,
                'plat' : plat,
                'userlist' : [acctid,],
            }
            #print recv_tuple
            return recv_tuple

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

