from common.mongo import MongoModel
from lib import get_ts

class CoinTypeModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_type'

    def get_keys(self):
        return 'area','plat','ts', 'type'

    def handle(self, recv_body):
        if recv_body:
            if not recv_body['data'].get('amount', 0) or \
               recv_body['data']['amount'] > 0:
                return
                
            try:
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                coin_type = recv_body['data']['extra']['consumetype']
                ts = recv_body['ts']
                amount = abs(recv_body['data']['amount'])
                new = str(recv_body['data']['extra']['new_yuanbao'])
                uid = str(recv_body['data']['Uid'])
            except KeyError as e:
                print 'Key error: ', str(e)
                print recv_body
                return
                
            plat = str(plat_arr[len(plat_arr) -2])
            record_key = '_'.join([uid, str(ts), new])

            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval='day'),
                'type' : coin_type
            }
                    
            __id = self.get_one(search)
            search['coin'] = amount
            if __id:
                userlist = __id['userlist']                
                mid = str(__id['_id'])
                search['userlist'] = __id['userlist']
                if record_key not in userlist:
                    search['userlist'].append(record_key)
                    search['coin'] += amount
                    self.update(mid, search)
                else:
                    return
            else:
                search['userlist'] = [record_key,]
                self.insert(search)

            if search.get('_id', 0):
               del search['_id'] 
            del search['userlist']

            search['ts'] = get_ts(ts, interval='hour')
            search['coin'] = amount

            return search
