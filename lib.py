import re
import json
import time
import logging

from configs.config import DB_NAME

def gamelog_parse(line):
    FORMAT = '%Y-%m-%d %H:%M:%S'
    m = re.match(r'(\w+)\t\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\t(.*)', line)
    if m:
        data = json.loads(m.group(3))    
        if data.get('opname', 0) and data.get('opno', 0):
            area = m.group(1)
            ts = time.strptime(m.group(2), FORMAT)
            ts = int(time.mktime(ts))
            global MAX, num
            gamelog = {
                'op' : {
                    'code' : data['opname'],
                    'id'   : data['opno']
                },
                'area' : area,
                'ts' : ts,
                'data' : data
            }
            return gamelog

def gamelog_filter(gamelog_tuple):
    global num
    opnode = ['login_logcount', 'signup_logcount', 'createrole_logcount', 
              'logout_logcount',
              'yuanbao_logchange', 'shop_subyuanbao', 
              'fuben_logchange', 'trunk_task_accept', 'trunk_task_finish', 
             ]
    if not gamelog_tuple['op']['code'] in opnode:
        return
    return gamelog_tuple

def get_ts(time_str = "", interval = 'hour'):
    if interval == 'hour':
        formatter = '%Y-%m-%d %H:00:00'
    else:
        formatter = '%Y-%m-%d'
    if not time_str:
        now = time.strftime(formatter, time.localtime())
    else:
        now = time_str

    return int(time.mktime(time.strptime(now, formatter)))


#def log(filename,  info = "start ..."):
#    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), os.path.abspath(filename), info)
    
def log_config():
    logger = logging.getLogger('online_analytics')
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler('online.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s]  - %(asctime)s -  %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

def get_db(db_key):
    if db_key:
        return DB_NAME[db_key]['db']

def get_collection(db_key):
    if db_key:
        return DB_NAME[db_key]['coll']


