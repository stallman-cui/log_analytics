from common.mongo import MongoModel
from lib import get_ts

class LoginDayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_login'

    def get_conf(self):
        conf = {
            'sub_conf' : ['login_hour'],
            'state' : 'login'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            area = recv_body['area']
            plat = recv_body['plat']
            ts = recv_body['ts']
            acctid = recv_body['acctid']
          
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval = 'day')
            }
            __id = self.get_one(search)
            if __id:
                userlist = __id['userlist']
                mid = str(__id['_id'])
                search['count'] = __id['count']
                if acctid not in userlist:
                    search['userlist'] = userlist
                    search['userlist'].append(acctid)
                    search['count'] += 1
                    self.update(mid, search)
                else:
                    return
            else:
                search['count'] = 1
                search['userlist'] = [acctid,]
                self.insert(search)

            if search.get('_id', 0):
               del search['_id'] 
            del search['userlist']
            search['acctid'] = acctid
            search['type'] = 'login'
            return search
