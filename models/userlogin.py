from common.mongo import MongoModel
from lib import get_ts

class LoginModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_login'

    def get_keys(self):
        return 'game','area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            try:
                area = recv_body['area']
                plat = recv_body['data']['corpid']
                acctid = recv_body['data']['acct']
            except KeyError:
                return

            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts()
            }
            __id = self.get_one(search)
            search['new'] = False
            if __id:
                userlist = __id['userlist']
                mid = str(__id['_id'])
                if acctid not in userlist:
                    search['userlist'] = userlist
                    search['userlist'].append(acctid)
                    search['count'] = __id['count'] + 1
                    self.update(mid, search)
                    search['new'] = True
            else:
                search['count'] = 1
                search['userlist'] = [acctid,]
                self.insert(search)
                search['new'] = True

            if search.get('_id', 0):
               del search['_id'] 
            search['type'] = 'login'
            return search
