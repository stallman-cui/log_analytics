import logging

from common.mongo import MongoModel
from lib import gamelog_parse, gamelog_filter

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

    def get_data(self):
        logger = logging.getLogger('online_analytics')
        gamelog = '/home/cui/log_analytics/gamelog.txt'
        #gamelog = 'gamelog_20150108.txt'
        #gamelog = '/home/cui/log_analytics/gamelog_2015-60.txt'
        result = []
        try:
            with open(gamelog, 'r') as f:
                for line in f:
                    line = gamelog_parse(line)
                    if line:
                        line = gamelog_filter(line)
                        if line:
                            result.append(line)
        except IOError as e:
            logger.error("read gamelog error: %s", str(e))
        #logger.error('gamelog: result: %s', result)
        return result
