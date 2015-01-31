#!/usr/bin/env python
# This program 
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

from common.mongo import MongoModel 

class AccountUserModel(MongoModel, object):
    def get_db(self):
        return 'mhgame'

    def get_collection(self):
        return 'user'
