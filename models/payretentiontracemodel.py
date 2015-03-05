from common.mongo import MongoModel
from models.paysummarymodel import PaySummaryModel
from configs.config import END_TOPO_SUCCESS

class PayRetentionTraceModel(MongoModel):
    def __init__(self):
        MongoModel.__init__(self)
        self.paysummarymodel = PaySummaryModel()

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['createrole'],
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
            createrole_list = recv_body['userlist']
            for i in range(0, 31):
                if i <= 7 or i == 14 or i == 30:
                    start = ts - i * 3600 * 24
                    search = {
                        'area' : area,
                        'plat' : plat,
                        'ts' : start
                    }
                    paysummary = self.paysummarymodel.get_one(search, {'userlist' : 1})
                    result = self.get_one(search, {'_id' : 1})

                    if paysummary:
                        if len(createrole_list) <= len(paysummary['userlist']):
                            user_fix = dict.fromkeys(x for x in createrole_list \
                                                     if x in paysummary['userlist'])
                        else:
                            user_fix = dict.fromkeys([x for x in  paysummary['userlist']\
                                                          if x in createrole_list])
                        if i > 0:
                            search[str(i) + '_retention'] = len(user_fix)
                        else:
                            search['create_role_count'] = len(createrole_list)
                            search['pay_user_count'] = len(user_fix)
                    else: # paysummary is emtpy
                        if i > 0:
                            search[str(i) + '_retention'] = 0
                        else:
                            search['create_role_count'] = len(createrole_list)
                            search['pay_user_count'] = 0

                    if result:
                        mid = str(result['_id'])
                        self.update(mid, search)
                    else:
                        search['game'] = game
                        self.insert(search)

            return END_TOPO_SUCCESS
