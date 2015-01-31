from common.mongo import MongoModel

class HostModel(MongoModel):
    def get_db(self):
        return 'sysop'

    def get_collection(self):
        return 'host'
