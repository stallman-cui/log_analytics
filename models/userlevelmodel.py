from common.mongo import MongoModel 
from lib import get_ts
from configs.config import END_TOPO_SUCCESS

class UserLevelModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_level'

    def get_keys(self):
        return 'game', 'area', 'plat'

    def get_conf(self):
        conf = {
            'sub_conf' : ['syncuser', ],
            'state' : 'userlevel'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            users = recv_body['userlist']
            levellist = {}
            for uid, info in users.items():
                grade = info['grade']
                if not levellist.get(grade, 0):
                    levellist[grade] = 1
                else:
                    levellist[grade] += 1

            search = {
                'game' : game,
                'area' : area,
                'plat' : plat,
                'leveldata' : levellist,
                'total_user' : len(levellist),
                'ts' : get_ts(info['ts'], interval='day')            
            }
            self.upsert(search)
            return END_TOPO_SUCCESS
