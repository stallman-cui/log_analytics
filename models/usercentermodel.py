from common.mongo import MongoModel 
from configs.config import END_TOPO_SUCCESS

class UserCenterModel(MongoModel):
    def get_db(self):
        return 'usercenter'

    def get_collection(self):
        return 'user'

    def get_keys(self):
        return 'area', 'plat', 'uid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['syncuser', ],
            'state' : 'usercenter'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            self.upsert(recv_body)
            return END_TOPO_SUCCESS
