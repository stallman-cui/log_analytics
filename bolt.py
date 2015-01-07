# Bolt represents a component that takes tuples as input and produces tuples
# as output.

class Bolt(object):
    ''' Bolt represents a component that takes tuples as 
    input and produces tuples as output.
    '''
    def prepare(self, conf, topology_context, output_collector):
        ''' Called when a task for this component is Initialized
        within a worker on the cluster.
            conf: The configuration for this spout.
            topology_context: The input and output information.
            output_collector: The collector is used to emit tuples from this spout.
        '''
        
    def execute(self, input):
        ''' Process a single tuple of input. '''

    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

