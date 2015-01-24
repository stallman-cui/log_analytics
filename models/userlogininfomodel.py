import pymongo
import time

from common.mongo import MongoModel
from configs.config import END_TOPO_SUCCESS

class UserLoginInfoModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_login_info'

    def get_keys(self):
        return 'area','plat', 'acctid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['login_logcount', 'logout_logcount'],
            'state' : 'userlogininfo'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            try:
                area = recv_body['area']
                acctid = str(recv_body['data']['acct'])
                log_type = recv_body['data']['type']
                ts = recv_body['ts']
                plat = str(recv_body['data']['corpid'])
            except KeyError:
                #print('KeyError: ', str(e))
                try:
                    plat = str(recv_body['data']['CorpId'])
                except KeyError:
                    return
            
            search = {
                'area' : area,
                'plat' : plat,
                'acctid' : acctid
            }

            result = self.get_list(search).sort('_id', pymongo.DESCENDING).limit(1)
            if result.count():
                for i in result:
                    result = i
                    mid = str(result['_id'])
            else:
                result = None

            #1.when type == signin: if result is empty, or login_ts and 
            #  logout_ts both not empty, so insert the record
            if log_type == 'signin' and \
               (not result or 
                (result.get('login_ts', 0) and result.get('logout_ts', 0) and (ts > result['login_ts']))):
                search['login_ts'] = ts
                search['ts'] = int(time.time())
                self.insert(search)
                return END_TOPO_SUCCESS
                
            #2.when type == signout: if result is empty, or login_ts and 
            #  logout_ts both not empty, so drop the record
            if log_type == 'signout' and \
               (not result or 
                (result.get('login_ts', 0) and (result.get('logout_ts', 0)))):
                return

            #3.when type == signin: if login_ts is not empty and 
            #  logout_ts is empty, so update the login_ts
            if log_type == 'signin' and \
               (result.get('login_ts', 0) and (not result.get('logout_ts', 0)) and (ts > result['login_ts'])):
                search['login_ts'] = ts
                search['ts'] = int(time.time())
                self.update(mid, search)
                return END_TOPO_SUCCESS

            #4.when type == signout: if login_ts is not empty and 
            #  logout_ts is empty, so update the logout_ts
            if log_type == 'signout' and \
               (result.get('login_ts', 0) and (not result.get('logout_ts', 0)) and (ts > result['logout_ts'])):
                search['logout_ts'] = ts
                search['ts'] = int(time.time())
                self.update(mid, search)
                return END_TOPO_SUCCESS
