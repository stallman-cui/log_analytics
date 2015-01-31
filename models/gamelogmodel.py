from common.mongo import MongoModel

class GamelogModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'gamelog'

    def get_conf(self):
        conf = {
            'state' : 'gamelog'
        }
        return conf
