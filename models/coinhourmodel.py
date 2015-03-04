from common.mongo import MongoModel
from analyticslib.lib import get_ts
from configs.config import END_TOPO_SUCCESS

class CoinHourModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_hour'

    def get_conf(self):
        conf = {
            'sub_conf' : ['coinfilter'],
            'state' : 'coinhour'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
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
                'ts' : get_ts(ts, interval='hour')
            }
            __id = self.get_one(search)
            search['coin'] = coin
            if __id:
                mid = str(__id['_id'])
                search['coin'] += __id['coin']
                self.update(mid, search)
            else:
                search['game'] = game
                self.insert(search)

        return END_TOPO_SUCCESS
