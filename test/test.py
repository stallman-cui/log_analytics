#!/usr/bin/env python
import os
import sys
import unittest
import time
import re

basedir, testdir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append("%s" % basedir)

from models.gamelogmodel import GamelogModel
from models.paymentmodel import PaymentModel
from models.loginmodel import LoginModel
from models.signupmodel import SignupModel
from models.payorderusermodel import PayorderUserModel

class TestPaymentModel(unittest.TestCase):
    def test_read_payment_not_empty(self):
        payment = PaymentModel().get_data()
        #print('payment: output %d results' % len(payment))
        self.failIf(not payment, 'payment data is empty')

class TestGamelogModel(unittest.TestCase):
    def test_read_gamelog_not_empty(self):
        gamelog = GamelogModel().get_data()
        #print('gamelog: output %d results' % len(gamelog))
        for i in gamelog:
            self.assertEqual(len(i), 4)
        self.failIf(not gamelog, 'gamelog data is empty')

class TestMongoModel(unittest.TestCase):
    def setUp(self):
        self.model = LoginModel()

    def tearDown(self):
        del self.model

    def test_connect_to_mongodb(self):
        result = self.model.get_list().count()
        #print('login record count:', result)
        self.failIf(not result, 'mongodb service is error')

class TestLoginModel(unittest.TestCase):
    def setUp(self):
        self.model = LoginModel()
        self.source_data = {
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

    def tearDown(self):
        del self.source_data

    def test_login_hanle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        userlist = result['userlist']
        self.assertIn(self.source_data['data']['acct'], userlist)
        self.assertEqual(result['type'], 'login')

class TestSignupModel(unittest.TestCase):
    def setUp(self):
        self.model = SignupModel()
        self.source_data = {
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
        del self.source_data

    def test_signup_hanle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        self.assertEqual(result['ts'], 1420646400)
        userlist = result['userlist']
        self.assertIn(self.source_data['data']['acct'], userlist)
        self.assertEqual(result['type'], 'signup')

class TestPayorderUserModel(unittest.TestCase):
    def setUp(self):
        self.model = PayorderUserModel()
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

    def test_payorderuser_handle_data(self):
        result = self.model.handle(self.source_data)
        self.assert_(result)
        self.assertEqual(len(result), 9)
        self.assertEqual(result['type'], 'payorderuser')
        self.assertEqual(result['count'], 2) 
        self.assertEqual(result['pay_amout'], 3.0)
        self.assertEqual(result['pay_count'], 2)

class TestTransfer(unittest.TestCase):
    def setUp(self):
        cmd = '%s/transfer.py %s' % (basedir, 'start')
        rv = os.system(cmd)
        self.assertEqual(rv, 0)
        self.pidfile = os.path.join(basedir, 'log.pid')
        self.logfile = os.path.join(basedir, 'online.log')
        time.sleep(6)
    
    def tearDown(self):
        cmd = '%s/transfer.py %s' % (basedir, 'stop')
        rv = os.system(cmd)
        self.assertEqual(rv, 0)
        try:
            os.remove(self.logfile)
        except OSError as e:
            print(str(e))
        
    def test_transfer_data_count(self):
        print('\n')
        log = file(self.logfile).read().lower()
        #print(log)
        gamelog_match = re.findall(r'\w*gamelogmodel\sread\w*', log)
        payment_match = re.findall(r'\w*paymentmodel\sread\w*', log)
        match = [gamelog_match, payment_match]
        for each_match in match:
            self.assertEqual(len(each_match), 2)
        
        all_spout_count = {}
        for i in ['gamelog', 'payment']:
            pattern = '\w*' + i + 'model\srecords\scount\s\d*'
            match = re.search(pattern, log)
            count = match.group(0).split()[3]
            all_spout_count[i] = int(count)
        print('all_spout_count: ', all_spout_count)
        
        all_bolt_count = {}
        for i in ['login', 'signup', 'createrole', 'payorderuser', 'server']:
            pattern = '\w*' + i + 'model\s* processed\w*'
            count = len(re.findall(pattern, log))
            all_bolt_count[i] = count

        print('all_bolt_count: ', all_bolt_count)
        self.assertEqual(all_spout_count['gamelog']+all_spout_count['payment'],
                         all_bolt_count['login'] + all_bolt_count['signup'] + 
                         all_bolt_count['createrole'] + all_bolt_count['payorderuser'])


if __name__ == '__main__':
    unittest.main()
