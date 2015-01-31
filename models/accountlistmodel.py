from common.mongo import MongoModel 

class AccountListModel(MongoModel):
    def get_db(self):
        return 'mhgame'

    def get_collection(self):
        return 'list'
