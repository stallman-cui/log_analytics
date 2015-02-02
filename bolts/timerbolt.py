import logging

from configs.config import END_TOPO_SUCCESS

class TimerBolt():
    ''' handle the login log from gamelog
    '''
    def __init__(self, model, topology_context='', output_collector=''):
        self.logger = logging.getLogger('online_analytics')
        self.model = model()
        self.num = 0
        
    def prepare(self, conf='', topology_context='', output_collector=''):
        ''' Called when a task for this component is Initialized
        within a worker on the cluster.
            conf: The configuration for this spout.
            topology_context: The input and output information.
            output_collector: The collector is used to emit tuples
            from this spout.
        '''

    def execute(self):
        ''' Process a single tuple of input. '''
        result = self.model.handle()
        if END_TOPO_SUCCESS == result:
            self.logger.debug('%-30s done the job',
                              self.model.__module__) 
        else:
            self.logger.debug('%-30s error',
                              self.model.__module__) 

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''
