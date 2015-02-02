import re
import json
import time
import logging
import os

from models.areamodel import AreaModel
from models.platmodel import PlatModel

opnode = ['login_logcount', 'signup_logcount', 'createrole_logcount', 
          'logout_logcount',
          'yuanbao_logchange', 'shop_subyuanbao', 
          'fuben_logchange', 'trunk_task_accept', 'trunk_task_finish', 
]
precise_format = '%Y-%m-%d %H:%M:%S'
hour_format = '%Y-%m-%d %H:00:00'
day_format = '%Y-%m-%d'
basedir, bin = os.path.split(__file__)

def gamelog_parse(line):
    m = re.match(r'(\w+)\t\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\t(.*)', line)
    if m:
        data = json.loads(m.group(3))    
        if data.get('opname', 0) and data.get('opno', 0):
            area = m.group(1)
            ts = time.strptime(m.group(2), precise_format)
            ts = int(time.mktime(ts))
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
    global opnode 
    if not gamelog_tuple['op']['code'] in opnode:
        return
    return gamelog_tuple

def get_ts(timestamp='', interval = 'hour'):
    if interval == 'hour':
        unit = 60 * 60
        now = int(timestamp) / unit * unit
    else:
        now = time.localtime(timestamp) # time array
        now = time.strftime(day_format, now) # time str
        now = time.strptime(now, day_format) # time array
        now = int(time.mktime(now)) # time stamp

    return now

def get_period_ts(time_str='', interval='hour'):
    if interval == 'hour':
        formatter = hour_format
        diff = 3599
    else:
        formatter = day_format
        diff = 24 * 3600 - 1
    if not time_str:
        time_str = time.strftime(formatter, time.localtime())
    start = int(time.mktime(time.strptime(time_str, formatter))) 
    ts = {
        'start' : start,
        'end' : start + diff
    }
    return ts
    
def log_config():
    log_file = os.path.join(basedir, 'online.log')
    #level = logging.INFO
    level = logging.DEBUG
    logger = logging.getLogger('online_analytics')
    logger.setLevel(level)
    
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('[%(levelname)s]  - %(asctime)s -  %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def set_game_area_plat():
    am = AreaModel()
    pm = PlatModel()
    areas = am.get_list()
    plats = pm.get_list()
    game_area = {}
    plat_id_name = {}
    for area in areas:
        game_area[str(area['_id'])] = area['game']
        
    for plat in plats:
        plat_id_name[plat['id']] = plat['name']

    game_area_plat = {
        'area' : game_area,
        'plat' : plat_id_name
    }
    with open(os.path.join(basedir, 'game_area_plat.json'), 'w') as f:
        json.dump(game_area_plat, f)

def get_game_area_plat():
    with open(os.path.join(basedir, 'game_area_plat.json'), 'r') as f:
        game_area_plat = json.load(f)
        return game_area_plat

