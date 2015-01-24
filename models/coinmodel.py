from coinhourmodel import CoinHourModel
from coindaymodel import CoinDayModel
from cointypemodel import CoinTypeModel
from configs.config import END_TOPO_SUCCESS

class CoinModel():
    def __init__(self):
        self.hour_model = CoinHourModel()
        self.day_model = CoinDayModel()
        self.type_model = CoinTypeModel()

    def get_conf(self):
        conf = {
            'sub_conf' : ['yuanbao_logchange'],
            'state' : 'coin'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            type_result = self.type_model.handle(recv_body)
            if type_result:
                self.hour_model.handle(type_result)
                self.day_model.handle(type_result)

                return END_TOPO_SUCCESS
