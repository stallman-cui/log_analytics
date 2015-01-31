from common.mongo import MongoModel
from configs.config import END_TOPO_SUCCESS

class PayorderDetailModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'pay_order'

    def get_keys(self):
        return 'area','plat', 'orderid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['yuanbao_logchange'],
            'state' : 'payorderdetail'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            if not recv_body['data']['extra'].get('reqstr', 0):
                return
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                orderid = recv_body['data']['extra']['reqstr']
                before_yuanbao = recv_body['data']['extra']['old_yuanbao']
                after_yuanbao = recv_body['data']['extra']['new_yuanbao']
                uid = str(recv_body['data']['Uid'])
                name = recv_body['data']['Name']
            except KeyError as e:
                print 'Key error: ', str(e)
                return

            plat = str(plat_arr[len(plat_arr) -2])
            search = {
                'game' : game,
                'area' : area,
                'plat' : plat,
                'orderid' : orderid,
                'paybeforeyuanbao' : before_yuanbao,
                'payafteryuanbao' : after_yuanbao,
                'Uid' : uid,
                'Name' : name
            }

            self.upsert(search)
            
            #return search
            return END_TOPO_SUCCESS
