from common.mongo import MongoModel
from lib import get_ts
from configs.config import END_TOPO_SUCCESS

class GameCopyModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'game_copy'

    def get_keys(self):
        return 'area','plat', 'ts'

    def get_conf(self):
        conf = {
            'sub_conf' : ['fuben_logchange'],
            'state' : 'fuben'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            if recv_body['data']['amount'] != -1:
                return
            try:    
                area = recv_body['area']
                plat = str(recv_body['data']['CorpId'])
                copyid = recv_body['data']['get_id']
                ts = get_ts(recv_body['ts'], interval='day')
                plat_arr = recv_body['data']['URS'].split('_')
                win = recv_body['data']['extra']['iswin']
                name = recv_body['data']['extra']['name']
            except KeyError:
                return

            acctid = plat_arr[0]            
            yes_search = {
                'area' : area,
                'plat' : plat,
                'level' : copyid,
                'ts' : ts - 3600 * 24
            }
            yes_result = self.get_one(yes_search)
            yes_enter = 0
            yes_pass = 0
            if yes_result:
                yes_enter = yes_result.get('enteruserlist', 0)
                yes_pass = yes_result.get('passuserlist', 0)

            search = {
                'area' : area,
                'plat' : plat, 
                'level' : copyid,
                'ts' : ts
            }
            tod_result = self.get_one(search)
            tod_enter = 0
            tod_pass = 0
            if tod_result:
                tod_enter = tod_result.get('enteruserlist', 0)
                tod_pass = tod_result.get('passuserlist', 0)

            if tod_enter:
                # it is not first time
                search['enteruserlist'] = tod_enter
                if acctid not in tod_enter:
                    search['enteruserlist'].append(acctid)
                else:
                    return
            elif yes_enter:
                search['enteruserlist'] = yes_enter
                if acctid not in yes_enter:
                    search['enteruserlist'].append(acctid)
            else:
                search['enteruserlist'] = [acctid, ]
            search['enter_user'] = len(search['enteruserlist'])

            if win == 1:
                if tod_pass:
                    search['passuserlist'] = tod_pass
                    if acctid not in tod_pass:
                        search['passuserlist'].append(acctid)
                    else:
                        return
                elif yes_pass:
                    search['passuserlist'] = yes_pass
                    if acctid not in yes_pass:
                        search['passuserlist'].append(acctid)
                else:
                    search['passuserlist'] = [acctid, ]
                search['pass_user'] = len(search['passuserlist'])

            if tod_result:
                mid = str(tod_result['_id'])
                self.update(mid, search)
            else:
                search['name'] = name
                search['level'] = copyid
                self.insert(search)
            
            return END_TOPO_SUCCESS            
