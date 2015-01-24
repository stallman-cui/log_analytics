from common.mongo import MongoModel
from lib import get_ts
from configs.config import END_TOPO_SUCCESS

class MainlineModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'mainline'

    def get_keys(self):
        return 'area','plat', 'ts', 'taskid'

    def get_conf(self):
        conf = {
            'sub_conf' : ['trunk_task_accept', 'trunk_task_finish'],
            'state' : 'mainline'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            if not recv_body['data'].get('task_id', 0):
                return
            try:
                area = recv_body['area']
                plat_arr = recv_body['data']['URS'].split('_')
                task_id = recv_body['data']['task_id']
                opcode = recv_body['op']['code']
                ts = recv_body['ts']
                task_name = recv_body['data']['task_name']
            except KeyError as e:
                print('KeyError: ', str(e))
                return

            arr_len = len(plat_arr)
            acctid = ''
            if arr_len > 2:
                for i in range(arr_len - 2):
                    acctid += str(plat_arr[i])
            plat = str(plat_arr[arr_len -2])

            yes_search = {
                'area' : area,
                'plat' : plat, 
                'taskid' : task_id,
                'ts' : get_ts(ts-3600*24, interval='day')
            }
            yes_result = self.get_one(yes_search)
            yes_accept = 0
            yes_finish = 0
            if yes_result:
                yes_accept = yes_result.get('acceptuserlist', 0)
                yes_finish = yes_result.get('finishuserlist', 0)

            search = {
                'area' : area,
                'plat' : plat, 
                'taskid' : task_id,
                'ts' : get_ts(ts, interval='day')
            }
            # find the yesterday trunk task userlist, if acctid not in, 
            # add the acctid in today trunk task userlist
            tod_result = self.get_one(search)
            tod_accept = 0
            tod_finish = 0
            if tod_result:
                tod_accept = tod_result.get('acceptuserlist', 0)
                tod_finish = tod_result.get('finishuserlist', 0)
            search['name'] = task_name

            if opcode == 'trunk_task_accept':
                if tod_accept:
                    search['acceptuserlist'] = tod_accept
                    if acctid not in tod_accept:
                        search['acceptuserlist'].append(acctid)
                elif yes_accept:
                    search['acceptuserlist'] = yes_accept
                    if acctid not in yes_accept:
                        search['acceptuserlist'].append(acctid)
                else:
                    search['acceptuserlist'] = [acctid, ]
                search['accept_user'] = len(search['acceptuserlist'])
                
            elif opcode == 'trunk_task_finish':
                if tod_finish:
                    search['finishuserlist'] = tod_finish
                    if acctid not in tod_finish:
                        search['finishuserlist'].append(acctid)
                elif yes_finish:
                    search['finishuserlist'] = yes_finish
                    if acctid not in yes_finish:
                        search['finishuserlist'].append(acctid)
                else:
                    search['finishuserlist'] = [acctid, ]
                search['finish_user'] = len(search['finishuserlist'])

            if tod_result:
                mid = str(tod_result['_id'])
                self.update(mid, search)
            else:
                self.insert(search)
                
            return END_TOPO_SUCCESS
