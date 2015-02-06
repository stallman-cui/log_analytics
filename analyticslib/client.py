import argparse
import os

import version

def option_parser(basedir):
    config = os.path.join(basedir, 'configs/config.py')
    log = os.path.join(basedir, 'log/online.log')
    pid = os.path.join(basedir, 'analytics.pid')
    ver = '%(prog)s ' + version.VERSION

    parser = argparse.ArgumentParser(description='online log analytics')
    
    parser.add_argument('-l', '--log', action='store', default=str(log),
                        dest='log_file', help='The output log file')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        dest='debug', help='The log LEVEL')

    parser.add_argument('-c', '--config', action='store', default=config,
                        dest='config_file', help="The config file")

    parser.add_argument('-p', '--pid', action='store', default=pid,
                        dest='pid_file', help='The pid file')

    parser.add_argument('-m', '--multi', action='store_true', default=False,
                        dest='multihost', help='Deployed system on multihost')

    parser.add_argument('-s', action='store', default='start',
                        dest='signal',
                        help='Control the analytics system.[start|stop|restart]')    
    parser.add_argument('-v', '--version', action='version', version=ver, 
                        help='Display the program version')
    return  parser.parse_args()
