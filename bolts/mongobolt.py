import zmq.green as zmq
import json
import logging
from bson.objectid import ObjectId
from pymongo import MongoClient

from configs.config import *
import lib
from bolts.bolt import Bolt

class MongoBolt(Bolt):
    ''' handle the Mongodb operation
    '''
    num = 0
    def __init__(self, name = 'default'):
        self.prepare()
        self.logger = logging.getLogger('online_analytics')
        self.conn = self.connection(name)

    def prepare(self, conf='', topology_context='', output_collector=''):
        self.context = zmq.Context()
        self.recv_socket = self.context.socket(zmq.SUB)
        self.recv_socket.connect("tcp://127.0.0.1:5001")
        self.topicfilter = [PUBTITLE['server'],]
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
            #self.logger.debug('mongo execute: %d ', MongoBolt.num)
            MongoBolt.num += 1

            db_key = recv_tuple['state']
            #recv_tuple['state'] = "mongo"
            fix_data = recv_tuple['body']
            self.insert(db_key, fix_data)
            self.logger.debug('%-10s processed messsage id: %d', 'Mongo', recv_tuple['id'])
            
    def cleanup(self):
        ''' Called when an IBolt is going to be shutdown. '''

    def connection(self, name):
        uri = DB_CONN['mongo_db'][name]['uri']
        self.prefix = DB_CONN['mongo_db'][name]['prefix']
        return MongoClient(uri)

    def insert(self, db_key, data):
        db = self.prefix + lib.get_db(db_key)
        coll = lib.get_collection(db_key)
        self.conn[db][coll].insert(data)

    def delete(self, id_str):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        self.conn[db][coll].remove(ObjectId(id_str))

    def update(self, id_str, change = {}):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        search = {'_id' : ObjectId(id_str)}
        return self.conn[db][coll].update(search, {'$set': change})

    def upsert(self, search, data):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        return self.conn[db][coll].update(search, data, upsert = True)
    
    def get_list(self, search = {}, display = {}):
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find(search, display, timeout = False)
        return self.conn[db][coll].find(search, timeout = False)

    def get_one(self, search = {}, display = {}):
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find_one(search, display)
        return self.conn[db][coll].find_one(search)

    def __del__(self):
        self.conn.close()
