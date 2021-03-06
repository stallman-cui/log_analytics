import subprocess
import time
import os

from spouts.basespout import BaseSpout
from models.gamelogmodel import GamelogModel
from models.hostmodel import HostModel
from configs.config import ssh_user
from analyticslib.lib import *

class GamelogSpout(BaseSpout):
    """ read the gamelog data,
    and send it
    """
    timer = 240
    
    def __init__(self):
        BaseSpout.__init__(self, model=GamelogModel)
        self.hm = HostModel()
    
    def next_tuple(self):
        self.logger.info('%-10s Starting read the data ...', 'Gamelog')
        basedir, bin = os.path.split(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(basedir, 'data')
        FORMAT = '%Y%m%d%H%M'
        time_now = time.strftime(FORMAT, time.localtime())
        time_stamp = (int(time.mktime(time.strptime(time_now, FORMAT))) / 300 - 1) * 300
        out_file = os.path.join(data_dir, 'gamelog_' + time.strftime('%Y%m%d%H%M', time.localtime(time_stamp)) + '.txt')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        if os.path.exists(out_file):
            os.remove(out_file)

        set_game_area_plat()
        areas = get_game_area_plat()['area']
        hosts = self.hm.get_list({'flag.available' : True})
        for host in hosts:
            host = host['id']
            command = ('t=$(expr $(date +%s) / 300 - 1);'
                       't=$(date --date @$(expr $t \* 300) +%Y%m%d%H%M);' 
                       'for g in /home/mhgame/games/*;' 
                       'do find $g/log/gamelog -name mh_$t.log | xargs sed -e "s/^/$(basename $g)\t/";' 
                       'done 2>/dev/null')
            remote_user_host = str(ssh_user) + '@' + host
            ssh = subprocess.Popen(["ssh", '-C', remote_user_host, command],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
            )
            for line in  ssh.stdout.readlines():
                line = gamelog_parse(line)
                if line:
                    valid_line = gamelog_filter(line)
                    if valid_line:
                        valid_line['game'] = areas[valid_line['area']]
                        message_tuple = {
                            'body' : valid_line,
                            'state' : valid_line['op']['code']
                        }
                        self.count += 1
                        self.socket.send_json(message_tuple)
                        ack_no = self.socket.recv_string()
                        if ack_no != 'Error':
                            self.ack(ack_no)
                        else:
                            self.fail(ack_no)

                    self.model.handle(line)


        self.logger.info('%-10s End the read data ...', 'Gamelog')
