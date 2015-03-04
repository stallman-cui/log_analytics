from common.mongo import MongoModel
from analyticslib.lib import get_ts
from configs.config import END_TOPO_SUCCESS

class CoinTypeModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_type'

    def get_conf(self):
        conf = {
            'sub_conf' : ['coinfilter'],
            'state' : 'cointype'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts', 'type'

    def handle(self, recv_body):
        if recv_body:
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                coin_type = recv_body['data']['extra']['consumetype']
                ts = recv_body['ts']
                coin = abs(recv_body['data']['amount'])
            except KeyError as e:
                print 'Key error: ', str(e)
                print recv_body
                return
                
            plat = str(plat_arr[len(plat_arr) -2])
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval='day'),
                'type' : coin_type
            }
            __id = self.get_one(search)
            search['coin'] = coin
            if __id:
                search['coin'] += __id['coin']
                mid = str(__id['_id'])
                self.update(mid, search)
            else:
                search['game'] = game
                self.insert(search)

            return END_TOPO_SUCCESS
