from common.mongo import MongoModel
from lib import get_ts

class CreateroleModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_create_role'

    def get_conf(self):
        conf = {
            'sub_conf' : ['createrole_logcount'],
            'state' : 'createrole'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            try:
                area = recv_body['area']
                plat = str(recv_body['data']['corpid'])
                acctid = str(recv_body['data']['acct'])
                ts = recv_body['ts']
            except KeyError:
                return
            search = {
                'area' : area,
                'plat' : str(plat),
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
                search['count'] = 1
                search['userlist'] = [acctid,]
                self.insert(search)

            if search.get('_id', 0):
               del search['_id'] 
            search['type'] = 'createrole'
            return search
