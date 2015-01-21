#!/usr/bin/env python
import etcd
import time

class Worker(object):
    def __init__(self):
        # host, port, version_prefix, read_timeout, allow_redirect ...
        self.client = etcd.Client(host='127.0.0.1', port=4001)
    
    def register(self, pid):
        # register itselt to etcd
        try:
            self.client.write('/analytics_root/worker', None, dir=True)
        except KeyError:
            pass
        self.client.write('/analytics_root/worker/{}'.format(pid), int(time.time()))

    def unregister(self, pid):
        # delete(self, key, recursive=None, dir=None, **kwdargs):
        self.client.delete('/analytics_root/worker/{}'.format(pid))
        
    
    def read_worker(self, pid):
        # Read the worker info by pid key
        try:
            return self.client.read('/analytics_root/worker/{}'.format(pid))
        except KeyError:
            print("the worker %s is not registed in etcd." % pid)

    def clean_up(self):
        try:
            self.client.delete('/analytics_root/worker', recursive=True, dir=True)
        except KeyError as e:
            print('I got a KeyError - rease "%s"' % str(e))

    def assignment(self):
        pass

    def update(self, pid, ts):
        self.client.write('/analytics_root/worker/{}'.format(pid), ts)
        
if __name__ == "__main__":
    new_worker = Worker()
    new_worker.clean_up()

    new_worker.register(100002)
    print new_worker.read_worker(100002)
    
    time.sleep(10)
    new_worker.unregister(100002)
    #new_worker.unregister()
