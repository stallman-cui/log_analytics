from common.mongo import MongoModel
from models.createroledaymodel import CreateroleDayModel
from configs.config import END_TOPO_SUCCESS

class PayTraceDayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace_day'

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

