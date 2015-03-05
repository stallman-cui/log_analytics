from common.mongo import MongoModel
from analyticslib.lib import get_ts

class UserPayFilterModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_user_list'

    def get_keys(self):
        return 'area','plat', 'uid', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['yuanbao_logchange'],
            'state' : 'userpayfilter'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            try:
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                ts = recv_body['ts']
                new = str(recv_body['data']['extra']['new_yuanbao'])
                uid = str(recv_body['data']['Uid'])
                amount = recv_body['data']['amount']
            except KeyError as e:
                print 'Key error: ', str(e)
                return

            plat = str(plat_arr[len(plat_arr) -2])
            record_key = '_'.join([str(ts), new, str(amount)])
            search = {
                'area' : area,
                'plat' : plat,
                'uid' : uid,
                'ts' : get_ts(ts, interval='day'),
            }
            result = self.get_one(search, {'userlist':1})
            if result:
                search['userlist'] = result['userlist']
                if record_key not in result['userlist']:
                    search['userlist'].append(record_key)
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    return
            else:
                search['userlist'] = [record_key, ]
                self.insert(search)

            return recv_body
