from common.mongo import MongoModel
from models.usercentermodel import UserCenterModel
from lib import get_ts, get_game_area_plat
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
            amount = yuanbao_amount / 10
            used_yuanbao = 0
            if yuanbao_amount < 0:
                used_yuanbao = -yuanbao_amount

            search = {
                'area' : area,
                'plat' : plat,
                'ts' : get_ts(ts, interval=3),
                'uid' : uid
            }
            result = self.get_one(search)

            user_search = {
                'area' : area,
                'uid' : uid
            }
            user_result = self.ucmodel.get_one(user_search)
            if user_result:
                search['rest_yuanbao'] = user_result['rest_yuanbao']
                search['reg_time'] = user_result['birthday']
                search['recent_login'] = user_result['login_time']

            if result:
                search['count'] = result['count'] + 1
                search['yuanbao'] = result['yuanbao'] + yuanbao_amount
                search['amount'] = result['amount'] + amount
                search['used_yuanbao'] = result['used_yuanbao'] + used_yuanbao
                mid = str(result['_id'])
                self.update(mid, search)
            else:
                search['game'] = game
                search['Grade'] = grade
                search['Name'] = name
                search['platname'] = plat_name
                search['count'] = 1
                search['yuanbao'] = yuanbao_amount
                search['amount'] = amount
                search['used_yuanbao'] = used_yuanbao
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
                    
                self.insert(search)
            
            return END_TOPO_SUCCESS
