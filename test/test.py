#!/usr/bin/env python
import os
import unittest
import time
import re
import sys
from random import randint

basedir, testdir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append(basedir)

from spouts.gamelogspout import GamelogSpout
from spouts.paymentspout import PaymentSpout

from analyticslib.lib import *

from models.signuphourmodel import SignupHourModel
from models.loginhourmodel import LoginHourModel
#from models.createrolehourmodel import CreateroleHourModel
from models.logindaymodel import LoginDayModel
from models.paysummarymodel import PaySummaryModel

class TestPaymentModel(unittest.TestCase):
    def test_read_payment_not_empty(self):
        payment = PaymentSpout()
        ts = get_period_ts(interval='day')
        search = { 
            'start' : ts['start'],
            'end' : ts['end'],
            'page.index' : -1
        }
        data = payment.get_user_payment_list(search)
        self.failIf(data['status'] == 500, 'Get payment data error')

class TestMongoModel(unittest.TestCase):
    def setUp(self):
        self.model = LoginDayModel()

    def tearDown(self):
        del self.model

    def test_connect_to_mongodb(self):
        result = self.model.get_list().count()
        #print('login record count:', result)
        self.failIf(not result, 'mongodb service is error')

class TestLoginHourModel(unittest.TestCase):
    def setUp(self):
        self.model = LoginHourModel()
        self.source_data = {
            'game' : 'dl',
            'area' : '5343a423dbdb67b036b3ee00',
            'data' : {
                'opno' : 1003,
                'server_name' : 'server1001',
                'corpid' : 2001,
                'acct' : '713565446',
                'opname' : 'login_logcount',
                'type' : 'signin'
            },
            'ts' : 1420684846,
            'op' : {
                'code' : 'login_logcount',
                'id' : 1003
            }
        }
        self.source_data['data']['acct'] = 'test_999999999999'
    def tearDown(self):
        search = {
            'game' : 'dl',
            'area' : '5343a423dbdb67b036b3ee00',
            'plat' : '2001',
            'ts' : 1420682400
        }
        loginhour = self.model.get_one(search)
        if self.source_data['data']['acct'] in loginhour['userlist']:
            loginhour['userlist'].remove(self.source_data['data']['acct'])
            mid = str(loginhour['_id'])
            self.model.update(mid, loginhour)
        
        del self.source_data

    def test_login_hour_hanle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        userlist = result['userlist']
        self.assertIn(self.source_data['data']['acct'], userlist)

class TestSignupHourModel(unittest.TestCase):
    def setUp(self):
        self.model = SignupHourModel()
        self.source_data = {
            'game' : 'dl',
            'area' : '5343a423dbdb67b036b3ee00',
            'data' : {
                'opno' : 1003,
                'server_name' : 'server1001',
                'corpid' : 2001,
                'acct' : '713565446',
                'opname' : 'signup_logcount',
                'type' : 'signin'
            },
            'ts' : 1420684846,
            'op' : {
                'code' : 'signup_logcount',
                'id' : 1003
            }
        }

    def tearDown(self):
        search = {
            'game' : 'dl',
            'area' : '5343a423dbdb67b036b3ee00',
            'plat' : '2001',
            'ts' : 1420682400
        }
        signuphour = self.model.get_one(search)
        if self.source_data['data']['acct'] in signuphour['userlist']:
            signuphour['userlist'].remove(self.source_data['data']['acct'])
            mid = str(signuphour['_id'])
            self.model.update(mid, signuphour)

        del self.source_data

    def test_signup_hour_hanle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        self.assertEqual(result['ts'], 1420682400)
        userlist = result['userlist']
        self.assertIn(self.source_data['data']['acct'], userlist)

class TestPaysummaryModel(unittest.TestCase):
    def setUp(self):
        self.model = PaySummaryModel()
        self.source_data = {
            'game' : 'dl',
            'area' : '549140c8dbdb67794fc0fa3b',
            'plat' : '2001',
            'ts' : 1420646400,
            'users' : {
                '3412825528' : {'times' : 1, 'amount' : 2.0},
                '3349885891' : {'times' : 1, 'amount' : 1.0}
            }
        }

    def tearDown(self):
        del self.source_data
        del self.model

    def test_paysummary_handle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        self.assertEqual(len(result), 9)
        self.assertEqual(result['type'], 'paysummary')
        self.assertEqual(result['count'], 2) 
        self.assertEqual(result['pay_amout'], 3.0)
        self.assertEqual(result['pay_count'], 2)

if __name__ == '__main__':
    unittest.main()
