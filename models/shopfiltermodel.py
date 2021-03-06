from common.mongo import MongoModel
from analyticslib.lib import get_ts

class ShopFilterModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'prop_user_list'

    def get_conf(self):
        conf = {
            'sub_conf' : ['shop_subyuanbao'],
            'state' : 'shopfilter'
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
                uid = recv_body['data']['Uid']
                buyitemno = recv_body['data']['buyitemno']
            except KeyError as e:
                print('KeyError: ', str(e))
                return

            plat = str(plat_arr[1])         
            acctid = plat_arr[0]
            record_key = '_'.join([str(ts), uid, str(buyitemno)])

            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval='day'),
                'buyitemno' : buyitemno
            }
            result = self.get_one(search)
            if result:
                search['filterlist'] = result['filterlist']
                search['userlist'] = result['userlist']
                if record_key not in result['filterlist']:
                    search['filterlist'].append(record_key)
                    if acctid not in result['userlist']:
                        search['userlist'].append(acctid)
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    return
            else:
                search['game'] = game
                search['userlist'] = [acctid, ]
                search['filterlist'] = [record_key, ]
                self.insert(search)
            
            return recv_body
