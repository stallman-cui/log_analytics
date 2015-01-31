from spouts.basespout import BaseSpout
from models.gamelogmodel import GamelogModel
from lib import *

class GamelogSpout(BaseSpout):
    """ read the gamelog data,
    and send it
    """
    def __init__(self):
        BaseSpout.__init__(self, model=GamelogModel)
    
    def next_tuple(self):
        self.logger.info('%-10s Starting read the data ...', 'Gamelog')
        set_game_area_plat()
        areas = get_game_area_plat()['area']
        gamelog = '/home/cui/log_analytics/gamelog.txt'
        gamelog = '/home/cui/log_analytics/gamelog_2015-60.txt'
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
