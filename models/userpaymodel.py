from common.mongo import MongoModel
from models.usercentermodel import UserCenterModel
from analyticslib.lib import get_ts, get_game_area_plat
from configs.config import END_TOPO_SUCCESS

class UserPayModel(MongoModel):
    def __init__(self):
        MongoModel.__init__(self)
        self.ucmodel = UserCenterModel()
        
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay'

    def get_keys(self):
        return 'area','plat', 'uid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['userpayfilter'],
            'state' : 'userpay'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                yuanbao_amount = recv_body['data']['amount']
                grade = recv_body['data']['Grade']
                uid = str(recv_body['data']['Uid'])
                name = recv_body['data']['Name']
                ts = recv_body['ts']
            except KeyError as e:
                print 'Key error: ', str(e)
                return

            plat = str(plat_arr[len(plat_arr) -2])
            plat_name = get_game_area_plat()['plat'][plat]
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval='day'),
                'uid' : uid
            }
            result = self.get_one(search)

            if not recv_body['data']['extra'].get('reqstr', 0):
                ## consume record, used_yuanbao
                if yuanbao_amount > 0:
                    return
                if result:
                    search['used_yuanbao'] = abs(yuanbao_amount)
                    if result.get('used_yuanbao', 0):
                        search['used_yuanbao'] += result['used_yuanbao']
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    search['used_yuanbao'] = abs(yuanbao_amount)
                    self.insert(search)
            else:
                ## charge record, count, yuanbao, amount
                user_search = {
                    'area' : area,
                    'uid' : uid
                }
                user_result = self.ucmodel.get_one(user_search)
                if user_result:
                    search['rest_yuanbao'] = user_result['rest_yuanbao']
                    search['reg_time'] = user_result['birthday']
                    search['recent_login'] = user_result['login_time']
                first_search = {
                    'area' : area,
                    'plat' : plat,
                    'uid' : uid,
                    'firstPayGrade' : {
                        '$exists' : 'true'
                    }
                }
                first_result = self.get_one(first_search, {'firstPayGrade':1})
                if first_result:
                    search['firstPayGrade'] = first_result['firstPayGrade']
                else:
                    search['firstPayGrade'] = grade
                if result:
                    search['game'] = game
                    search['grade'] = grade
                    search['name'] = name
                    search['platname'] = plat_name
                    search['count'] = 1
                    search['yuanbao'] = yuanbao_amount
                    search['amout'] = yuanbao_amount / 10
                    if result.get('count', 0):
                        search['count'] += result['count']
                        search['yuanbao'] += result['yuanbao']
                        search['amout'] += result['amout']
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    search['game'] = game
                    search['grade'] = grade
                    search['name'] = name
                    search['platname'] = plat_name
                    search['count'] = 1
                    search['yuanbao'] = yuanbao_amount
                    search['amout'] = yuanbao_amount / 10
                    self.insert(search)
            
            return END_TOPO_SUCCESS
