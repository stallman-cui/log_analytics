#!/usr/bin/env python
import etcd
import time
import json
import config
import yaml

class topology(object):
    def __init__(self, ):
        # host, port, version_prefix, read_timeout, allow_redirect ...
        self.client = etcd.Client(host='127.0.0.1', port=4001)
        self.conf = config.topology_file

    def create_topology(self, topology = "default"):
        # write(self, key, value, ttl=None, dir=False, append=False, **kwdargs)

        client = self.client
        graph = self._read_json()
        client.write('/analytics_root', None, dir=True)
        client.write('/analytics_root/topology', None, dir=True)
        client.write('/analytics_root/topology/{}'.format(topology),  graph)

    def read_topology(self, topology = "default"):
        # read(self, key, **kwdargs)
        client = self.client
        key = '/analytics_root/topology/{}'.format(topology)
        return client.read(key)

    def clean_up(self):
        try:
            self.client.delete('/analytics_root', recursive=True, dir=True)
        except KeyError as e:
            print('I got a KeyError - rease "%s"' % str(e))

    def _write_json(self):
        graph = {
            'gamelog' : ['login_logcount', 'signup_logcount', 'create_role_logcount'],
            'login_logcount' : ['server'],
            'signup_logcount' : ['server'],
            'create_role_logcount' : ['server']
        }
        try:
            with open(self.conf, 'w') as f:
                json.dump(graph, f)
        except IOError as e:
            print('Read the topology file error: ', str(e))

    def _read_json(self):
        try:
            with open(self.conf, 'r') as f:
                return json.load(f)
        except IOError as e:
            print('Read the topology file error: ', str(e))

if __name__ == "__main__":
    new_topology = topology()
    new_topology.clean_up()

    print('Create new topology log_topology...')
    new_topology.create_topology("log_topology")
    print('Read the log_topology...')
    result = new_topology.read_topology("log_topology")
    result = yaml.load(result.value)
    print(json.dumps(result, indent=3))
