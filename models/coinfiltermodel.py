from common.mongo import MongoModel
from lib import get_ts

class CoinFilterModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_user_list'

    def get_conf(self):
        conf = {
            'sub_conf' : ['yuanbao_logchange'],
            'state' : 'coinfilter'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            if not recv_body['data'].get('amount', 0) or \
               recv_body['data']['amount'] > 0:
                return
            try:
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                ts = recv_body['ts']
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
            }
            result = self.get_one(search)
            if result:
                search['userlist'] = result['userlist']                
                if record_key not in search['userlist']:
                    search['userlist'].append(record_key)
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    return
            else:
                search['userlist'] = [record_key, ]
                self.insert(search)

            return recv_body
