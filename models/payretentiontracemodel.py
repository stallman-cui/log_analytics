from common.mongo import MongoModel
from models.createroledaymodel import CreateroleDayModel
from configs.config import END_TOPO_SUCCESS

class PayRetentionTraceModel(MongoModel):
    def __init__(self):
        MongoModel.__init__(self)
        self.createmodel = CreateroleDayModel()

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['paysummary'],
            'state' : 'payretentiontrace'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            ts = recv_body['ts']

            # update retention
            pay_user_list = recv_body['userlist']
            for i in range(0, 31):
                if i <= 7 or i == 14 or i == 30:
                    start = ts - i * 3600 * 24
                    search = {
                        'area' : area,
                        'plat' : plat,
                        'ts' : start
                    }
                    createrole = self.createmodel.get_one(search, {'userlist' : 1})
                    if createrole:
                        if len(createrole['userlist']) <= len(pay_user_list):
                            user_fix = dict.fromkeys([x for x in createrole['userlist'] \
                                                      if x in pay_user_list])
                        else:
                            user_fix = dict.fromkeys([x for x in pay_user_list \
                                                          if x in createrole['userlist']])
                        if not(len(user_fix)):
                            continue

                        result = self.get_one(search, {'_id' : 1})
                        search['create_role_count'] = len(createrole['userlist'])
                        if i > 0:
                            search[str(i) + '_retention'] = len(user_fix)
                        else:
                            search['pay_user_count'] = len(user_fix)

                        if result:
                            mid = str(result['_id'])
                            self.update(mid, search)
                        else:
                            search['game'] = game
                            self.insert(search)
                            
                    else: # createrole is emtpy
                        continue

            return END_TOPO_SUCCESS
