#!/usr/bin/env python
topology_file = '/home/cui/log_analytics/configs/topology.etc'

PUBTITLE = {
    'login_logcount' : '1001',
    'signup_logcount' : '1002', 
    'createrole_logcount' : '1003',
    'yuanbao_logchange' : '1004',
    'logout_logcount' : '1005',
    'shop_subyuanbao' : '1006',
    'fuben_logchange' : '1007',
    'trunk_task_accept' : '1008',
    'trunk_task_finish' : '1009',
    'login' : '2004',
    'signup' : '2005',
    'createrole' : '2006',
    'server' : '2007',
    'payment' : '2008',
    'payorderuser' : '2009',
    'coin' : '2010',
}

END_TOPO_SUCCESS = 'end'

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
