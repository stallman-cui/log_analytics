from common.mongo import MongoModel
from models.logindaymodel import LoginDayModel
from configs.config import END_TOPO_SUCCESS
from analyticslib.lib import *

class ServerStartTimeModel(MongoModel):
    timer = 60 * 60

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'server_start_time'

    def get_keys(self):
        return 'game','area','plat'

    def handle(self):
        login_model = LoginDayModel()
        areas = get_game_area_plat()['area']
        ts = get_ts(int(time.time()), interval='day')
        for area in areas:
            search = {
                'area' : area,
                'ts' : ts
            }
            result = login_model.get_list(search, {'area':1, 'plat':1})
            for login_record in result:
                plat = login_record['plat']
                search = {
                    'game' : areas[area],
                    'area' : area,
                    'plat' : plat
                }
                result = self.get_one(search)
                if not result:
                    search['server_start_time'] = ts
                    self.insert(search)

        return END_TOPO_SUCCESS
