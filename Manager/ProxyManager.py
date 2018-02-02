# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py
   Description :
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3:
-------------------------------------------------
"""
__author__ = 'JHao'

import random

from Util import EnvUtil
from DB.DbClient import DbClient
from Util.GetConfig import GetConfig
from Util.LogHandler import LogHandler
from ProxyGetter.getFreeProxy import GetFreeProxy
from geoip import geolite2

class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.config = GetConfig()
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):
        """
        fetch proxy into Db by ProxyGetter
        :return:
        """
        for proxyGetter in self.config.proxy_getter_functions:
            # fetch raw proxy
            for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
                if proxy:
                    self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy['ip']))
                    self.db.changeTable(self.useful_proxy_queue)
                    if self.db.exists(proxy['ip']):
                        continue
                    self.db.changeTable(self.raw_proxy_queue)
                    proxy['country'] = self.get_ip_country(proxy['ip'])
                    self.db.put(proxy)

    def get_ip_country(self, ip):
        match = geolite2.lookup(ip)
        return match.country if match else None

    def get(self, filters):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.random_one(filters)

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool as list
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        return self.db.getAll()

    def clean(self):
        self.db.clean()

    def getNumber(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_queue = self.db.getNumber()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}

if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()
