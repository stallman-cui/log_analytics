#!/usr/bin/env python
import etcd
import os
import time

class worker(object):
    def __init__(self):
        # host, port, version_prefix, read_timeout, allow_redirect ...
        self.client = etcd.Client(host='127.0.0.1', port=4001)
        self.pid = os.getpid()
    
    def register(self):
        # register itselt to etcd

        self.client.write('/analytics_root/worker', None, dir=True)
        self.client.write('/analytics_root/worker/{}'.format(self.pid), int(time.time()))

    def unregister(self):
        # delete(self, key, recursive=None, dir=None, **kwdargs):
        self.client.delete('/analytics_root/worker/{}'.format(self.pid))
        
    
    def read_worker(self):
        # Read the worker info by pid key
        try:
            return self.client.read('/analytics_root/worker/{}'.format(self.pid))
        except KeyError:
            print("the worker %s is not registed in etcd." % self.pid)

    def clean_up(self):
        try:
            self.client.delete('/analytics_root/worker', recursive=True, dir=True)
        except KeyError as e:
            print('I got a KeyError - rease "%s"' % str(e))

    def assignment(self):
        pass

if __name__ == "__main__":
    new_worker = worker()
    new_worker.clean_up()

    new_worker.register()
    print new_worker.read_worker()
    time.sleep(30)    
    new_worker.unregister()
