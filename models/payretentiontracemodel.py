from common.mongo import MongoModel
from models.createroledaymodel import CreateroleDayModel
from configs.config import END_TOPO_SUCCESS

class PayRetentionTraceModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['paysummary', 'createrole'],
            'state' : 'payretentiontrace'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            area = recv_body['area']
            plat = recv_body['plat']
            ts = recv_body['ts']
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : ts
            }
            # update today's create_role_count and pay_user_count
            if recv_body['type'] == 'createrole':
                search['create_role_count'] = recv_body['count']
                result = self.get_one(search, {'_id' : 1})
                if result:
                    mid = str(result['_id'])
                    self.update(mid, search)
                else:
                    self.insert(search)

            # update retention
            if recv_body['type'] == 'paysummary':      
                pay_user_list = recv_body['userlist']
                createmodel = CreateroleDayModel()
                for i in range(0, 31):
                    if i <= 7 or i == 14 or i == 30:
                        start = ts - i * 3600 * 24
                        search = {
                            'area' : area,
                            'plat' : plat,
                            'ts' : start
                        }
                        createrole = createmodel.get_one(search, {'userlist' : 1})
                        if createrole:
                            if len(createrole['userlist']) <= len(pay_user_list):
                                user_fix = dict.fromkeys([x for x in createrole['userlist'] \
                                                          if x in pay_user_list])
                            else:
                                user_fix = dict.fromkeys([x for x in pay_user_list \
                                                          if x in createrole['userlist']])
                            if not(len(user_fix)):
                                continue

                            search['create_role_count'] = len(createrole['userlist'])
                            if i > 0:
                                search[str(i) + '_retention'] = len(user_fix)
                            else:
                                search['pay_user_count'] = len(user_fix)

                            result = self.get_one(search, {'_id' : 1})
                            if result:
                                mid = str(result['_id'])
                                self.update(mid, search)
                            else:
                                self.insert(search)
                            
                        else: # createrole is emtpy
                            continue

            return END_TOPO_SUCCESS
