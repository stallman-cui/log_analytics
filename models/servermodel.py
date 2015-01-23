from common.mongo import MongoModel
from configs.config import END_TOPO_SUCCESS

class ServerModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'server'
    
    def get_conf(self):
        conf = {
            'sub_conf' : ['login', 'signup', 'createrole', 'payorderuser',],
            'state' : 'server'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            log_type = recv_body['type']

            search = {
                'area' : recv_body['area'],
                'plat' : recv_body['plat'],
                'ts' : recv_body['ts'],
            }

            __id = self.get_one(search)
            count = recv_body['count']

            if log_type == 'login':
                search['active'] = count
            elif log_type == 'signup':
                search['reg'] = count
            elif log_type == 'createrole':
                search['create_role'] = count
            elif log_type == 'payorderuser':
                search['pay_user'] = count
                search['pay_count'] = recv_body['pay_count']
                search['pay_amout'] = recv_body['pay_amout']

            if __id:
                mid = str(__id['_id'])
                self.update(mid, search)
            else:
                self.insert(search)

            #if search.get('_id', 0):
            #   del search['_id'] 
            return END_TOPO_SUCCESS
