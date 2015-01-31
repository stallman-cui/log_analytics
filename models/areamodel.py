from common.mongo import MongoModel
from bson.objectid import ObjectId

class AreaModel(MongoModel):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'area'

    def get_by_idstr(self, id):
        return self.get_one({'_id' : ObjectId(id)})
