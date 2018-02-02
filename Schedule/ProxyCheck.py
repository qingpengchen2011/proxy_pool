# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ProxyCheck
   Description :   多线程验证useful_proxy
   Author :        J_hao
   date：          2017/9/26
-------------------------------------------------
   Change Activity:
                   2017/9/26: 多线程验证useful_proxy
-------------------------------------------------
"""
__author__ = 'J_hao'

import sys
from time import sleep
from threading import Thread

sys.path.append('../')

from Util.utilFunction import validUsefulProxy
from Manager.ProxyManager import ProxyManager
from Util.LogHandler import LogHandler

FAIL_COUNT = 1  # 校验失败次数， 超过次数删除代理


class ProxyCheck(ProxyManager, Thread):
    def __init__(self):
        ProxyManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check')

    def run(self):
        self.db.changeTable(self.useful_proxy_queue)
        while True:
            proxy = self.db.pop()
            if proxy:
                addr = "%s:%s" % (proxy.get('ip'), proxy.get('port'))
                if validUsefulProxy(addr):
                    self.log.info('ProxyCheck: {} validation pass'.format(addr))
                else:
                    self.log.info('ProxyCheck: {} validation fail'.format(addr))
                    self.db.delete(proxy['ip'])
            sleep(20)

if __name__ == '__main__':
    p = ProxyCheck()
    p.run()
