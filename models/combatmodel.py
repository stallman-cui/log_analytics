from common.mongo import MongoModel 
from configs.config import END_TOPO_SUCCESS

class CombatModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'viji'

    def get_keys(self):
        return 'game', 'area', 'plat'

    def get_conf(self):
        conf = {
            'sub_conf' : ['syncuser', ],
            'state' : 'combat'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            users = recv_body['userlist']
            
            userlist = []
            for uid, info in users.items():
                urs_arr = info['URS'].split('_')
                acctid = ''
                size = len(urs_arr)
                if size > 2:
                    for i in range(0, size - 2):
                        acctid += str(urs_arr[i])
                else:
                    acctid = urs_arr[0]

                userlist.append({
                    'Uid' : uid,
                    'acctid' : acctid,
                    'role_name' : info['name'],
                    'Score' : info['score'],
                    'Grade' : info['grade'],
                    'reg_day' : info['birthday'],
                    'login_time' : info['login_time']
                })
                
            search = {
                'game' : game,
                'area' : area,
                'plat' : plat,
                'userlist' : userlist
            }
            self.upsert(search)
            return END_TOPO_SUCCESS
