from common.mongo import MongoModel

class GamelogModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'gamelog'

    def get_keys(self):
        return 'area', 'ts'

    def get_conf(self):
        conf = {
            'state' : 'gamelog'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            self.insert(recv_body)

