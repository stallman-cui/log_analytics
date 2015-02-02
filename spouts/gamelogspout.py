import subprocess
import time
import os

from spouts.basespout import BaseSpout
from models.gamelogmodel import GamelogModel
from models.hostmodel import HostModel
from lib import *

class GamelogSpout(BaseSpout):
    """ read the gamelog data,
    and send it
    """
    def __init__(self):
        BaseSpout.__init__(self, model=GamelogModel)
        self.hm = HostModel()
    
    def next_tuple(self):
        self.logger.info('%-10s Starting read the data ...', 'Gamelog')
        basedir, bin = os.path.split(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(basedir, 'data')
        out_file = os.path.join(data_dir, 'gamelog_' + time.strftime('%Y%m%d%H%M', time.localtime()) + '.txt')

        if os.path.exists(out_file):
            os.remove(out_file)

        f = open(out_file, 'a')
        print out_file
        set_game_area_plat()
        areas = get_game_area_plat()['area']
        hosts = self.hm.get_list({'flag.available' : True})
        hosts = ['s30.machine.millionhero.com', 's1.tdl.millionhero.com']
        for host in hosts:
            #host = host['id']
            command = 'ls -l'
            #command = ('t=$(expr $(date +%s) / 300 - 1);'
            #           't=$(date --date @$(expr $t \* 300) +%Y%m%d%H%M);' 
            #           'for g in /home/mhgame/games/*;' 
            #           'do find $g/log/gamelog -name mh_$t.log | xargs sed -e "s/^/$(basename $g)\t/";' 
            #           'done 2>/dev/null')
            ssh = subprocess.Popen(["ssh", "zwcui@%s" % host, command],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
            )
            print host
            for line in  ssh.stdout.readlines():
                #print(line)
                f.write(str(line))
        f.close()
            
        #gamelog = '/home/cui/log_analytics/gamelog.txt'
        gamelog = '/home/cui/log_analytics/gamelog_2015-60.txt'
        #gamelog = out_file
        try:
            with open(gamelog, 'r') as f:
                for line in f:
                    line = gamelog_parse(line)
                    if line:
                        line = gamelog_filter(line)
                        if line:
                            line['game'] = areas[line['area']]
                            message_tuple = {
                                'body' : line,
                                'state' : self.conf['state']
                            }
                            self.count += 1
                            self.socket.send_json(message_tuple)
                            ack_no = self.socket.recv_string()
                            if ack_no != 'Error':
                                self.ack(ack_no)
                            else:
                                self.fail(ack_no)
        except IOError as e:
            self.logger.error("read gamelog error: %s", str(e))

        self.logger.info('%-10s End the read data ...', 'Gamelog')
