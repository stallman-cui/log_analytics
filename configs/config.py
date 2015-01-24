#!/usr/bin/env python
topology_file = '/home/cui/log_analytics/configs/topology.etc'

PUBTITLE = {
    # gamelog's op.code
    'login_logcount' : '1001',
    'signup_logcount' : '1002', 
    'createrole_logcount' : '1003',
    'yuanbao_logchange' : '1004',
    'logout_logcount' : '1005',
    'shop_subyuanbao' : '1006',
    'fuben_logchange' : '1007',
    'trunk_task_accept' : '1008',
    'trunk_task_finish' : '1009',

    # design by own
    'login' : '2001',
    'signup' : '2002',
    'createrole' : '2003',
    #'server' : '2004',
    'payment' : '2005',
    'paysummary' : '2006',
    #'payorderdetail' : '2007',
    #'coin' : '2008',
    #'userlogininfo' : '2009',
    #'mainline' : '2010',
    'payretentiontrace' : '2011',
}

END_TOPO_SUCCESS = 200
END_TOPO_DROP = 300

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
