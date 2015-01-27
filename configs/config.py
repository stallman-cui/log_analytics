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
    'login_hour' :     '2001',
    'createrole_hour': '2002',
    'signup_hour' :    '2003',
    'login' :          '2004',
    'signup' :         '2005',
    'createrole' :     '2006',
    #'server' :        '2007',
    'payment' :        '2008',
    'paysummary' :     '2009',
    #'payorderdetail': '2010',
    'coinfilter' :     '2011',
    'cointype' :       '2012',
    'coinhour' :       '2013',
    #'coin' :          '2014',
    #'userlogininfo' : '2015',
    #'mainline' :      '2016',
    'payretentiontrace':'2017',
    'shopfilter' :      '2018',
    #'shop' :           '2019',
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
