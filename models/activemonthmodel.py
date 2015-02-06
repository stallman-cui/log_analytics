import time

from common.mongo import MongoModel
from models.areamodel import AreaModel
from models.logindaymodel import LoginDayModel
from models.serverstarttimemodel import ServerStartTimeModel
from configs.config import END_TOPO_SUCCESS
from analyticslib.lib import *

class ActiveMonthModel(MongoModel):
    timer = 60 * 60 * 24 * 30

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_activity_month'
    
    def get_keys(self):
        return 'area','plat','ts'

    def handle(self):
        login_model = LoginDayModel()
        area_model = AreaModel()
        sstm = ServerStartTimeModel()
        now = int(time.time())
        areas = area_model.get_list()
        for area_item in areas:
            for plat in area_item['plats']:
                game = area_item['game']
                area = str(area_item['_id'])
                search = {
                    'game' : game,
                    'area' : area,
                    'plat' : plat
                }
                result = sstm.get_one(search)
                if result:
                   server_start_time = result['server_start_time'] 
                else:
                    continue
                    
                start = server_start_time
                end = start + 3600 * 24 * 30 -1
                re_time = []
                while start <= now:
                    re_time.append({'start':start, 'end':end})
                    start = end + 1
                    end = start + 3600 * 24 * 30 -1

                for each_time in re_time:
                    search['ts'] = {
                        '$gte' : each_time['start'],
                        '$lte' : each_time['end']
                    }
                    userlist = []
                    result = login_model.get_list(search)
                    for i in result:
                        userlist += i['userlist']
                        userlist = list(set(userlist))

                    fix_data = {
                        'game' : game,
                        'area' : area,
                        'plat' : plat,
                        'ts' : start,
                        'ac_user' : len(userlist)
                    }
                    self.upsert(fix_data)

        return END_TOPO_SUCCESS
