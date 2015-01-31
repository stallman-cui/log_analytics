import sys
import os
basedir, bin = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.insert(0, basedir)

from common.mongo import MongoModel

class PlatModel(MongoModel):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'plat'

    def get_by_id(self, plat_id):
        search = {
            'id' : plat_id
        }
        return self.get_one(search)

if __name__ == "__main__":
    print PlatModel().get_by_id('1000')['name']
