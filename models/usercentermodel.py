from common.mongo import MongoModel 
from configs.config import END_TOPO_SUCCESS

class UserCenterModel(MongoModel):
    def get_db(self):
        return 'usercenter'

    def get_collection(self):
        return 'user'

    def get_keys(self):
        return 'area', 'plat', 'uid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['syncuser', ],
            'state' : 'usercenter'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            userlist = recv_body['userlist']
            
            for uid, info in userlist.items():
                search = {
                    'game' : game,
                    'area' : area,
                    'plat' : plat,
                    'uid' : uid,
                    'urs' : info['urs'],
                    'login_time' : info['login_time'],
                    'grade' : info['grade'],
                    'name' : info['name'],
                    'birthday' : info['birthday'],
                    'score' : info['score'],
                    'rest_yuanbao' : info['rest_yuanbao'],
                    'ts' : info['ts']                    
                }
                self.upsert(search)
                    
            return END_TOPO_SUCCESS
