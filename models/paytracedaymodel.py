from common.mongo import MongoModel
from models.createroledaymodel import CreateroleDayModel
from models.paysummarymodel import PaySummaryModel
from configs.config import END_TOPO_SUCCESS
from analyticslib.lib import get_ts

class PayTraceDayModel(MongoModel):
    def __init__(self):
        MongoModel.__init__(self)
        self.createmodel = CreateroleDayModel()
        self.paymodel = PaySummaryModel()

    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace_day'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['payment'],
            'state' : 'paytraceday'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            game = recv_body['game']
            area = recv_body['area']
            plat = recv_body['plat']
            ts = get_ts(recv_body['ts'], interval='day')
            users = recv_body['users']
        else:
            return

        search = {
            'area' : area,
            'plat' : plat,
            'ts' : ts
        }
        createrole = self.createmodel.get_one(search, {'userlist' : 1})
        create_userlist = []
        if createrole:
            create_userlist = createrole['userlist']

        pay_userlist = []
        for kuser, vuser in users.items():
            pay_userlist.append(kuser)
        
        search = {'area' : area, 'plat' : plat}
        before_pay = self.paymodel.get_list(search, {'userlist':1})
        before_pay_userlist = []
        for each_pay in before_pay:
            before_pay_userlist += each_pay['userlist']
        before_pay_userlist = set(before_pay_userlist)

        # recharge in today and create role today
        paytoday_createrole_userlist = dict.fromkeys(x for x in pay_userlist \
                                                     if x in create_userlist)
        # recharge in today and create role before
        paybefore_createrole_userlist = dict.fromkeys(x for x in pay_userlist if \
                                                      x not in create_userlist)
        old_pay_user = dict.fromkeys(x for x in paybefore_createrole_userlist \
                                     if x in before_pay_userlist)
        new_pay_user = dict.fromkeys(x for x in paybefore_createrole_userlist \
                                     if x not in before_pay_userlist)
        search = {
            'game' : game,
            'area' : area,
            'plat' : plat,
            'ts' : ts
        }
        search['old_pay_user_count'] = len(old_pay_user)
        search['old_pay_user_count_a'] = 0
        search['old_pay_user_amout'] = 0

        search['new_pay_user_count'] = len(new_pay_user)
        search['new_pay_user_count_a'] = 0
        search['new_pay_user_amout'] = 0
        
        search['today_total_pay_user_count'] = len(pay_userlist)
        search['today_createrole_pay_user_count'] = len(paytoday_createrole_userlist)
        search['today_createrole_count'] = len(create_userlist)

        for each_user in old_pay_user:
            search['old_pay_user_count_a'] += users[each_user]['times']
            search['old_pay_user_amout'] += users[each_user]['amount']
            
        for each_user in new_pay_user:
            search['new_pay_user_count_a'] += users[each_user]['times']
            search['new_pay_user_amout'] += users[each_user]['amount']

        self.upsert(search)
        return END_TOPO_SUCCESS
