from common.mongo import MongoModel
from analyticslib.lib import get_ts

class UserPayFilterModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_user_list'

    def get_keys(self):
        return 'area','plat', 'uid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['yuanbao_logchange'],
            'state' : 'userpayfilter'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            if not recv_body['data']['extra'].get('reqstr', 0):
                return
            try:
                area = recv_body['area']
                plat = str(recv_body['data']['CorpId'])
                orderid = recv_body['data']['extra']['reqstr']
                ts = recv_body['ts']
            except KeyError as e:
                print 'Key error: ', str(e)
                return

            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval=3),
            }
            result = self.get_one(search, {'userlist':1})
            record_key = '_'.join([str(ts), str(orderid)])
            if result:
                search['userlist'] = result['userlist']
                if record_key not in result['userlist']:
                    search['userlist'].append(record_key)
                else:
                    return
            else:
                search['userlist'] = [record_key, ]

            return recv_body
