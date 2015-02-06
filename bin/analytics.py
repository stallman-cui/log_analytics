#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
import sys
import logging
import os
import time
import multiprocessing
import gevent

basedir, bin = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.insert(0, basedir)

from analyticslib.daemon import Daemon
from analyticslib.transfer import Transfer
from analyticslib.client import option_parser
from analyticslib.worker import Worker
from analyticslib.lib import log_config

from bolts.basebolt import BaseBolt
from bolts.timerbolt import TimerBolt
from allmodel import bolt_models_1
from allmodel import bolt_models_2
from allmodel import bolt_timer_models
from allmodel import all_spouts

class Analytics(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)
        self.logger = logging.getLogger('online_analytics')
        self.pidfile = pidfile
        self.transfer = Transfer()

    def update_status(self):
        pid = int(file(self.pidfile).read().strip())
        worker = Worker()
        while True:
            worker.update(pid, int(time.time()))
            gevent.sleep(1)

    # generate a data process
    def make_bolt(self, model):
        bolt = BaseBolt(model)
        while True:
            bolt.execute()
            gevent.sleep(0)

    def make_timer_bolt(self, model, timer):
        bolt = TimerBolt(model)
        if timer:
            while True:
                gevent.sleep(600)
                bolt.execute()
                gevent.sleep(timer)

    def make_spout(self, model, timer):
        spout = model()
        if timer:
            while True:
                spout.next_tuple()
                gevent.sleep(timer)

    def init_base(self):
        thread = []
        thread.append(gevent.spawn(self.transfer.receiver))
        thread.append(gevent.spawn(self.transfer.sender))
        #thread.append(gevent.spawn(self.update_status))
        gevent.joinall(thread)

    def init_spout(self):
        coroutines = []
        for each_spout in all_spouts:
            timer = each_spout.timer
            coroutines.append(gevent.spawn(self.make_spout, each_spout, timer))
  
        gevent.joinall(coroutines)
        
    def init_bolt_1(self):
        coroutines = []
        for each_model in bolt_models_1:
            coroutines.append(gevent.spawn(self.make_bolt, each_model))
        gevent.joinall(coroutines)

    def init_bolt_2(self):
        coroutines = []
        for each_model in bolt_models_2:
            coroutines.append(gevent.spawn(self.make_bolt, each_model))
        gevent.joinall(coroutines)

    def init_timer_bolt(self):
        coroutines = []
        for each_model in bolt_timer_models:
            timer = each_model.timer
            coroutines.append(gevent.spawn(self.make_timer_bolt, each_model, timer))
        gevent.joinall(coroutines)

    def run(self):
        base_process = multiprocessing.Process(name='base_thread', target=self.init_base)
        bolt_process_1 = multiprocessing.Process(name='bolt1', target=self.init_bolt_1)
        bolt_process_2 = multiprocessing.Process(name='bolt2', target=self.init_bolt_2)
        bolt_timer_process = multiprocessing.Process(name='timerbolt', target=self.init_timer_bolt)
        spout_process = multiprocessing.Process(name='spout', target=self.init_spout)
        
        base_process.start()
        bolt_process_1.start()
        bolt_process_2.start()
        bolt_timer_process.start()
        spout_process.start()
        
if __name__ == "__main__":
    args = option_parser(basedir)
    print args
    if args.debug == True:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    log_config(args.log_file, log_level)
    online_analytics = Analytics(args.pid_file)
    
    control_signal = args.signal
    if control_signal == 'start':
        online_analytics.start()
    elif control_signal == 'stop':
        online_analytics.stop()
    elif control_signal == 'restart':
        online_analytics.restart()
    else:
        print('unkown control_signal: [start|stop|restart]')
