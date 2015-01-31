from common.mongo import MongoModel
from configs.config import END_TOPO_SUCCESS

class CoinHourModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_hour'

    def get_conf(self):
        conf = {
            'sub_conf' : ['cointype'],
            'state' : 'coinhour'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            ts = recv_body['ts']
            coin = recv_body['coin']
                
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : ts
            }
            __id = self.get_one(search)
            search['coin'] = coin
            search['game'] = game
            if __id:
                mid = str(__id['_id'])
                search['coin'] += __id['coin']
                self.update(mid, search)
            else:
                self.insert(search)

        return END_TOPO_SUCCESS
