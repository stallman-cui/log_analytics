import time

from common.mongo import MongoModel 
from configs.config import END_TOPO_SUCCESS

class CombatModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'viji'

    def get_keys(self):
        return 'area', 'plat'

    def handle(self, recv_body):
        if recv_body:
            for karea, varea in recv_body.items():
                for kplat, vplat in varea.items():
                    plat_users = []
                    for user in vplat:
                        search = {
                            'Uid' : user['uid'],
                            'acctid' : user['acctid'],
                            'role_name' : user['name'],
                            'Score' : user['score'],
                            'Grade' : user['grade'],
                            'reg_day' : user['birthday'],
                            'login_time' : user['login_time'] 
                        }
                        game = user['game']
                        plat_users.append(search)

                    fix_data = {
                        'game' : game,
                        'area' : karea,
                        'plat' : kplat,
			'ts' : int(time.time()),
                        'userlist' : plat_users
                    }
                    self.upsert(fix_data)

            return END_TOPO_SUCCESS
