import time

from spouts.basespout import BaseSpout
from models.syncusermodel import SyncUserModel
from models.accountlistmodel import AccountListModel
from models.accountusermodel import AccountUserModel
from lib import *

class SyncUserSpout(BaseSpout):
    def __init__(self):
        BaseSpout.__init__(self, model=SyncUserModel)
        self.usermodel = AccountUserModel('002_h_user')
        self.listmodel = AccountListModel('002_h_user')
        
    def next_tuple(self):
        self.logger.info('%-10s Starting read the data ...', 'Syncuser')
        set_game_area_plat()
        areas = get_game_area_plat()['area']
        ts = int(time.time())
        for area in areas.keys():
            game = areas[area]
            search = {
                'area' : area
            }
            display = {
                '_id' : 0,
                'area' : 1,
                'data.user.URS' : 1,
                'data.user.LoginTime' : 1,
                'data.user.Grade' : 1,
                'data.user.Name' : 1,
                'data.user.Birthday' : 1,
                'data.user.TotalScore' : 1,
                'data.user.Score' : 1
            }
            user_data = self.usermodel.get_list(search, display)
            for user_item in user_data:
                user = user_item['data']['user']
                urs_arr = user['URS'].split('_')
                if 'dl' == game:
                    user['Score'] = user['TotalScore']

                search = {
                    'data.URS' : user['URS']
                }
                
                list_data = self.listmodel.get_one(search, {'data.YuanBao':1})
                rest_yuanbao = 0
                if list_data:
                    rest_yuanbao = list_data['data']['YuanBao']
                size = len(urs_arr)
                print urs_arr
                acctid = ''
                if size > 2:
                    for i in range(0, size - 2):
                        acctid += urs_arr[i]
                else:
                    acctid = urs_arr[0]
                plat = str(urs_arr[size - 2])

                search = {
                    'game' : game,
                    'area' : area,
                    'plat' : plat,
                    'acctid' : acctid,
                    'login_time' : user['LoginTime'],
                    'grade' : user['Grade'],
                    'name' : user['Name'],
                    'birthday' : user['Birthday'],
                    'score' : user['Score'],
                    'rest_yuanbao' : rest_yuanbao,
                    'ts' : ts
                }
                
                message_tuple = {
                    'body' : search,
                    'state' : self.conf['state']
                }
                self.count += 1
                self.socket.send_json(message_tuple)
                ack_no = self.socket.recv_string()
                if ack_no != 'Error':
                    self.ack(ack_no)
                else:
                    self.fail(ack_no)

        self.logger.info('%-10s End read the data ...', 'Syncuser')
