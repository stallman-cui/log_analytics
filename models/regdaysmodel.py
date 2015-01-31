from common.mongo import MongoModel

class RegDaysModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'reg_days'
