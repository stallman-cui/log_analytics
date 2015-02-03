from common.mongo import MongoModel 
from models.usercentermodel import UserCenterModel
from models.combatmodel import CombatModel
from configs.config import END_TOPO_SUCCESS
from lib import *

class UserLevelModel(MongoModel):
    timer = 60 * 60 * 24

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_level'

    def get_keys(self):
        return 'area', 'plat'

    def handle(self):
        usercenter_model = UserCenterModel()
        combat_model = CombatModel()
        users = usercenter_model.get_list()
        levellist = {}
        userlist = {}
        for user in users:
            area = user['area']
            plat = user['plat']
            grade = str(user['grade'])
            if not levellist.get(area, 0):
                levellist[area] = {
                    plat : {
                        grade : 1
                    }
                }
                userlist[area] = {
                    plat : [user,]
                }

            elif not levellist.get(plat, 0):
                levellist[area][plat] = {
                    grade : 1
                }
                userlist[area][plat] = [user,]
            else:
                levellist[area][plat][grade] += 1
                userlist[area][plat].append(user)

        areas = get_game_area_plat()['area']        
        ts = get_ts(int(time.time(), interval='day'))
        for karea, varea in levellist.items():
            for kplat, vplat in varea.items():
                user_count = 0
                for level_num in vplat.values():
                    user_count += level_num
                search = {
                    'game' : areas[karea],
                    'area' : karea,
                    'plat' : kplat,
                    'leveldata' : vplat,
                    'total_user' : user_count,
                    'ts' : ts
                }
                self.upsert(search)
                
                # combat model update data
                # this sub the seach to mongodb
                # just here special
                combat_model.handle(userlist)

        return END_TOPO_SUCCESS
