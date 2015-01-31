from common.mongo import MongoModel
from lib import get_ts

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
            if not recv_body['data'].get('amount', 0) or \
               recv_body['data']['amount'] > 0:
                return
                
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                coin_type = recv_body['data']['extra']['consumetype']
                ts = recv_body['ts']
                amount = abs(recv_body['data']['amount'])
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
            search['coin'] = amount
            search['game'] = game
            if __id:
                search['coin'] += amount
                mid = str(__id['_id'])
                self.update(mid, search)
            else:
                self.insert(search)

            if search.get('_id', 0):
               del search['_id'] 

            search['ts'] = get_ts(ts, interval='hour')
            search['coin'] = amount

            return search
