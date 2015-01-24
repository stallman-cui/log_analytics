from common.mongo import MongoModel

class PaySummaryModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'pay_order_user_list'
    
    def get_conf(self):
        conf = {
            'sub_conf' : ['payment'],
            'state' : 'paysummary'
        }
        return conf

    def get_keys(self):
        return 'area','plat','ts'

    def handle(self, recv_body):
        if recv_body:
            try:
                game = recv_body['game']
                area = recv_body['area']
                plat = recv_body['plat']
                ts = recv_body['ts']
                users = recv_body['users']
            except KeyError as e:
                print("KeyError: ", str(e))
                return

            pay_amout = 0
            pay_count = 0
            userlist = []
            for kuser, vuser in users.items():
                userlist.append(kuser)
                pay_count += vuser['times']
                pay_amout += vuser['amount']

            fix_data = {
                'game' : game,
                'area' : area, 
                'plat' : str(plat),
                'ts' : ts,
                'count' : len(users),
                'userlist' : userlist,
                'pay_amout' : pay_amout,
                'pay_count' : pay_count,
            }

            self.upsert(fix_data)

            fix_data['type'] = 'paysummary'

            if fix_data.get('_id', 0):
               del fix_data['_id'] 
            return fix_data
