import time

from common.mongo import MongoModel
from models.servermodel import ServerModel
from configs.config import END_TOPO_SUCCESS
from analyticslib.lib import get_ts

class ActiveDayModel(MongoModel):
    timer = 60 * 60 * 24

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_activity_day'
    
    def get_keys(self):
        return 'area','plat','ts'

    def handle(self):
        server = ServerModel()
        today = get_ts(int(time.time()), interval='day')
        yesterday = today - 3600 * 24
        for ts in [today, yesterday]:
            search = {
                'ts' : ts
            }
            result = server.get_list(search)
            for each_server in result:
                if each_server.get('active', 0):
                    ac_user = each_server['active']
                    if each_server.get('create_role', 0):
                        new_ac_user = each_server['create_role']
                    else:
                        new_ac_user = 0
                
                    search['game'] = each_server['game']
                    search['area'] = each_server['area']
                    search['plat'] = each_server['plat']
                    search['ac_user'] = ac_user
                    search['new_ac_user'] = new_ac_user 
                    search['new_ac_rate'] = round(float(new_ac_user) / ac_user * 100, 2)
                    search['old_ac_user'] = ac_user - new_ac_user
                    search['old_ac_rate'] = 100 - search['new_ac_rate']

                    self.upsert(search)

        return END_TOPO_SUCCESS
