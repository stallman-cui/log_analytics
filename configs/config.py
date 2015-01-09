#!/usr/bin/env python
topology_file = 'topology.etc'

PUBTITLE = {
    'login_logcount' : '1001',
    'signup_logcount' : '1003', 
    'createrole_logcount' : '1004',
    'login' : '1005',
    'signup' : '1006',
    'createrole' : '1007',
    'server' : '1008',
}


DB_CONN = {
    'mongo_db' : {
        'default' : {
            'uri' : 'mongodb://127.0.0.1:27017',
            'prefix' : 'mhmob_'
        },

        '002_h_user' : {
            'uri' : 'mongodb://119.146.203.248:27017',
            'prefix' : ''
        }
    },

    'ghoko' : {
        'secret' : 'mhis1,000kheros',
        'url' : 'http://127.0.0.1:3080'
    }   
}

DB_NAME = {
    'area' : {'db' : 'game', 'coll' : 'area'},
    'plat' : {'db' : 'game', 'coll' : 'plat'},
    'host' : {'db' : 'sysop', 'coll' : 'host'},

    'gamelog' : {'db' : 'analytics', 'coll' : 'gamelog'},
    'login'   : {'db' : 'analytics', 'coll' : 'user_login'},
    'signup' : {'db' : 'analytics', 'coll' : 'user_signup'},
    'createrole' : {'db' : 'analytics', 'coll' : 'user_create_role'},
    'server_start_time' : {'db' : 'analytics', 'coll' : 'server_start_time'},
    'server' : {'db' : 'analytics', 'coll' : 'server'},
    'mainline' : {'db' : 'analytics', 'coll' : 'mainline'},
    'payorder' : {'db' : 'analytics', 'coll' : 'pay_order'},
    'prop_user_list' : {'db' : 'analytics', 'coll' : 'prop_user_list'},
}
