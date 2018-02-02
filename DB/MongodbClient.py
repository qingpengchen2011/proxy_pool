# coding: utf-8
"""
-------------------------------------------------
   File Name：    MongodbClient.py
   Description :  封装mongodb操作
   Author :       JHao netAir
   date：          2017/3/3
-------------------------------------------------
   Change Activity:
                   2017/3/3:
                   2017/9/26:完成对mongodb的支持
-------------------------------------------------
"""
__author__ = 'Maps netAir'

import random
from pymongo import MongoClient

class MongodbClient(object):
    def __init__(self, name, host, port):
        self.name = name
        self.client = MongoClient(host, port)
        self.db = self.client.proxy

    def changeTable(self, name):
        self.name = name

    def get(self, proxy):
        data = self.db[self.name].find_one({'ip': proxy})
        return data['num'] if data != None else None

    def put(self, proxy):
        if not self.exists(proxy['ip']):
            self.db[self.name].insert(proxy)

    def pop(self):
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            self.delete(data['ip'])
            return data
        return None

    def delete(self, value):
        self.db[self.name].remove({'ip': value})

    def getAll(self):
        return self.db[self.name].find()

    def clean(self):
        self.client.drop_database('proxy')

    def random_one(self, filters):
        if filters.has_key('anony'):
            if filters['anony'] == '1':
                filters['anony'] = {'$in': ['高匿', '普匿']}
            else:
                del filters['anony']

        if filters.has_key('foreign'):
            if filters['foreign'] == '1':
                filters['country'] = { '$ne': 'CN' }
            else:
                filters['country'] = 'CN'

        cursor = self.db[self.name].find(filters, {'_id': 0})
        count = cursor.count()
        if count == 0:
            return None
        return cursor.skip(random.randint(0, count - 1)).limit(1)[0]

    def delete_all(self):
        self.db[self.name].remove()

    def update(self, key, value):
        self.db[self.name].update({'ip': key}, {'$inc': {'num': value}})

    def exists(self, key):
        return True if self.db[self.name].find_one({'ip': key}) != None else False

    def getNumber(self):
        return self.db[self.name].count()


if __name__ == "__main__":
    db = MongodbClient('first', 'localhost', 27017)
    # db.put('127.0.0.1:1')
    # db2 = MongodbClient('second', 'localhost', 27017)
    # db2.put('127.0.0.1:2')
    print(db.pop())
