import re
import json
import time

FORMAT = '%Y-%m-%d %H:%M:%S'

def gamelog_parse(line):
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
