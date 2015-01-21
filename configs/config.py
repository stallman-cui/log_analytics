#!/usr/bin/env python
topology_file = '/home/cui/log_analytics/configs/topology.etc'

PUBTITLE = {
    'login_logcount' : '1001',
    'signup_logcount' : '1003', 
    'createrole_logcount' : '1004',
    'login' : '1005',
    'signup' : '1006',
    'createrole' : '1007',
    'server' : '1008',
    'payment' : '1009',
    'payorderuser' : '1010',
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
