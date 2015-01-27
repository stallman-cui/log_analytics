from common.mongo import MongoModel
from lib import get_ts
from configs.config import END_TOPO_SUCCESS

class ShopModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'prop'

    def get_conf(self):
        conf = {
            'sub_conf' : ['shopfilter'],
            'state' : 'shop'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts', 'buyitemno'

    def handle(self, recv_body):
        if recv_body:
            try:
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                buyitemno = recv_body['data']['buyitemno']
                total = recv_body['data']['subyuanbao'] 
                count = recv_body['data']['count']
                ts = recv_body['ts']
                name = recv_body['data']['buyitemname']
            except KeyError as e:
                print('KeyError: ', str(e))
                return
                
            plat = str(plat_arr[1])
            search = {
                'area' : area,
                'plat' : plat,
                'buyitemno' : buyitemno,
                'ts' : get_ts(ts, interval='day')
            }
            result = self.get_one(search)
            if result:
                search['count'] = result['count'] + count
                search['buy_count'] = result['buy_count'] + 1
                search['user_count'] = result['user_count'] + 1
                mid = result['_id']
                self.update(mid, search)
            else:
                search['name'] = name
                search['buyitemno'] = buyitemno
                search['price'] = total / count
                search['user_count'] = 1
                search['buy_count'] = 1
                search['count'] = count
                self.insert(search)

            return END_TOPO_SUCCESS
