from common.mongo import MongoModel
from models.createroledaymodel import CreateroleDayModel
from configs.config import END_TOPO_SUCCESS

class LoginRetentionModel(MongoModel):
    def __init__(self):
        MongoModel.__init__(self)
        self.createmodel = CreateroleDayModel()

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_retention'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['login'],
            'state' : 'loginretentiontrace'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            area = recv_body['area']
            plat = recv_body['plat']
            ts = recv_body['ts']
            acctid = recv_body['acctid']
            search = {
                'area' : area,
                'plat' : plat,
                'ts' : ts
            }
            for i in range(0, 31):
                if i <= 7 or i == 14 or i == 30:
                    start = ts - i * 3600 * 24
                    search = {
                        'area' : area,
                        'plat' : plat,
                        'ts' : start
                    }
                    createrole = self.createmodel.get_one(search, {'userlist':1})
                    if not createrole:
                        continue

                    result = self.get_one(search)
                    if result:
                        if i > 0:
                            if acctid in createrole['userlist']:
                                search[str(i) + 'retention'] = 1
                                if result.get(str(i) + 'retention', 0):
                                    search[str(i) + 'retention'] += result[str(i) + 'retention']
                            else:
                                continue
                        else: 
                            search['user'] = len(createrole['userlist'])

                        mid = str(result['_id'])
                        self.update(mid, search)
                                
                    else:
                        self.insert(search)

            return END_TOPO_SUCCESS
