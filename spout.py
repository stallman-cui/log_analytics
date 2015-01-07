# spout is the core class for implementing spouts. A Spout is responsible
# for feeding messages into the topology for processing.


class Spout(object):

    def open(self, conf, topology_context, output_collector):
        ''' Called when a task for this component is initialized 
        within a worker on the cluster
            conf: the configuration for this spout
            topology_context: the input and output information
            output_collector: the collector is used to emit tuples from this spout
        '''
        
    def close(self):
        ''' Called when an spout is going to be shutdown. '''
        
    def activate(self):
        ''' Called when a spout has been activated out of a deactivated mode. '''
        
    def deactivate(self):
        ''' Called when a spout has been deactivated'''
        
    def next_tuple(self):
        ''' When this method is called, the spout emit tuples to the output collector. '''
        
    def ack(self, msg_id):
        ''' The tuple emiited by this spout with the msg_id has been fully processed. '''

    def fail(self, msg_id):
        ''' The tuple emitted by this spout with the msg_id has filed to be fully processed. '''
        
