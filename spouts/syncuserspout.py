import time

from spouts.basespout import BaseSpout
from modes.syncusermodel import SyncUserModel
from accountlistmodel import AccountListModel
from accountusermodel import AccountUserModel
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
        for area in areas.keys():
            search = {
                'area' : area
            }
            display = {
                '_id' : 0,
                'area' : 1,
                'data.user.Uid' : 1,
                'data.user.URS' : 1,
                'data.user.LoginTime' : 1,
                'data.user.Grade' : 1,
                'data.user.Name' : 1,
                'data.user.Birthday' : 1,
                'data.user.TotalScore' : 1,
                'data.user.Score' : 1
            }
            userlist = {}
            user_data = self.usermodel.get_list(search, display)
            for user_item in user_data:
                user = user_item['data']['user']
                urs_arr = user['URS'].split('_')
                plat = str(urs_arr[len(urs_arr) - 2])
                if 'dl' == game:
                    user['Score'] = user['TotalScore']

                search = {
                    'data.URS' : user['URS']
                }
                
                list_data = self.listmodel.get_one(search, {'data.YuanBao':1})
                rest_yuanbao = list_data['data']['YuanBao']
                ts = int(time.time())
                uid = str(user['Uid'])
                if not userlist.get(area, 0):
                    userlist[area] = {
                        plat : {
                            uid : {
                                'urs' : user['URS'],
                                'login_time' : user['LoginTime'],
                                'grade' : user['Grade'],
                                'name' : user['Name'],
                                'birthday' : user['Birthday'],
                                'score' : user['Score'],
                                'rest_yuanbao' : rest_yuanbao,
                                'ts' : ts,
                            }
                        }
                    }
                elif not userlist[area].get(plat, 0):
                    userlist[area][plat] = {
                        uid : {
                            'urs' : user['URS'],
                            'login_time' : user['LoginTime'],
                            'grade' : user['Grade'],
                            'name' : user['Name'],
                            'birthday' : user['Birthday'],
                            'score' : user['Score'],
                            'rest_yuanbao' : rest_yuanbao,
                            'ts' : ts,
                        }
                    }
                else:
                    userlist[area][plat][uid] = {
                        'urs' : user['URS'],
                        'login_time' : user['LoginTime'],
                        'grade' : user['Grade'],
                        'name' : user['Name'],
                        'birthday' : user['Birthday'],
                        'score' : user['Score'],
                        'rest_yuanbao' : rest_yuanbao,
                        'ts' : ts,
                    }

        for karea, varea in userlist.items():
            for kplat, vplat in varea.items():
                search = {
                    'game' : areas[karea],
                    'area' : karea,
                    'plat' : kplat,
                    'userlist' : vplat
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

        self.logger.info('%-10s Starting read the data ...', 'Syncuser')
