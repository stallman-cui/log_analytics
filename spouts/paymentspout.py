import time
import hashlib
import pycurl
import urllib
import json
import cStringIO

from configs.config import DB_CONN as db_config
from spouts.basespout import BaseSpout
from models.paymentmodel import PaymentModel
from lib import get_period_ts

class PaymentSpout(BaseSpout):
    def __init__(self):
        BaseSpout.__init__(self, model=PaymentModel)
        self.__ch = pycurl.Curl()
        self.__ch.setopt(pycurl.CONNECTTIMEOUT, 5)
        self.__ch.setopt(pycurl.FOLLOWLOCATION, True)
        self.__secret = db_config['ghoko']['secret']

    def call(self, url, query = {}, param = {}):
        buf = cStringIO.StringIO()
        self.__ch.setopt(pycurl.WRITEFUNCTION, buf.write)
        #print 'param: ', json.dumps(param, indent=3)
        host = 'https://pay.millionhero.com'
        ts = str(int(time.time()))
        sign = hashlib.md5(url + ts + self.__secret ).hexdigest()
        url = '{0}{1}?ts={2}&sign={3}&{4}'.format(host, url, ts, sign, urllib.urlencode(query))
        self.__ch.setopt(pycurl.URL, url)
        self.__ch.setopt(pycurl.USERAGENT, 'MH Client')
        self.__ch.setopt(pycurl.SSL_VERIFYHOST, False)
        self.__ch.setopt(pycurl.SSL_VERIFYPEER, False)

        if len(param):
            self.__ch.setopt(pycurl.POST, True)
            self.__ch.setopt(pycurl.POSTFIELDS, json.dumps(param))
        try:
            self.__ch.perform()
            result = {
                'status' : self.__ch.getinfo(pycurl.HTTP_CODE),
                'body' : buf.getvalue()
            }
        except pycurl.error as e:
            errno, errstr = e
            result = {'status' : 500, 'body' :  errstr}
        return result

    def get_user_payment_list(self, data):
        url = '/b/e'
        params = {}

        if 'game' in data.keys():
            params['game'] = data['game']

        if 'plat' in data.keys():
            params['plat'] = data['plat']
                    
        if 'area' in data.keys():
            params['area'] = data['area']
            
        if 'acct' in data.keys():
            params['user'] = data['acct']

        if 'start' in data.keys():
            params['ts'] = {
                'start' :  data['start']
            }

        if 'end' in data.keys():
            params['ts']['end'] = data['end']

        if 'page.index' in data.keys():
            params['page'] = {
                'index': data['page.index']
            }

        return self.call(url, {}, params)

    def next_tuple(self):
        self.logger.info('%-10s Starting read the data ...', 'Payment')
        #ts = get_period_ts()
        ts = {'start': 1420646400, 'end':1420732799}
        search = { 
            'start' : ts['start'],
            'end' : ts['end'],
            'page.index' : -1
        }
        data = self.get_user_payment_list(search)
        if data['status'] != 500:
            try:
                pmresult = json.loads(data['body'])
            except ValueError as e:
                self.logger.error('ValueError: %s', str(e))
                return

            user_pay_list = {}
            game_info = {}
            for d in pmresult:
                game = d['game']
                area = d['area']
                plat = d['plat']
                if not area in game_info.keys():
                    if not game in user_pay_list.keys():
                        user_pay_list[game] = {}

                    user_pay_list[game][area] = {
                        plat : {
                            d['user'] : {
                                'times' : 1,
                                'amount' : float(d['rmb'])
                            }
                        }
                    }
                    game_info[area] = 1
                elif not plat in user_pay_list[game][area].keys():
                    user_pay_list[game][area][plat] = {
                        d['user'] : {
                            'times' : 1,
                            'amount' : float(d['rmb'])
                        }
                    }
                elif not d['user'] in user_pay_list[game][area][plat]:
                    user_pay_list[game][area][plat][d['user']] = {
                        'times' : 1,
                        'amount' : float(d['rmb'])
                    }
                else:
                    user_pay_list[game][area][plat][d['user']]['times'] += 1
                    user_pay_list[game][area][plat][d['user']]['amount'] += float(d['rmb'])


            for kgame, vgame in user_pay_list.items():
                for karea, varea in vgame.items():
                    for kplat, vplat in varea.items():
                        search = {
                            'game' : kgame,
                            'area' : karea,
                            'plat' : str(kplat),
                            'ts' : ts['start'],
                            'users': vplat
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

        self.logger.info('%-10s End the read ...', 'Payment')
