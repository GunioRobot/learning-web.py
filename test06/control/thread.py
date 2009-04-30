# -*- coding:utf-8 -*-

# スレッドの内容、各レスの表示

import web
import os
import sys

from model import threadandres
from config import conf

class thread(object):
    u'''
    スレッド本体に関する処理
    '''
    def __init__(self, dbname=conf.DATABASE_PATH):
        self.db = threadandres.threadandres(dbname)

    def takeRecordAll(self):
        u'''
        すべてのレコードを取得する
        '''
        result = self.db.takeRecordAll()
        return result

    def threadIdToTakeRecord(self, thread_id):
        u'''
        スレッドIDを元にレスを求める
        '''
        result = self.db.threadIdToTakeRecord(thread_id)
        return result

    def threadIdAndLimitToTakeRecord(self, thread_id,
                                     start, length):
        u'''
        スレッドIDを指定、且つ取得範囲を指定する
        '''
        result = self.db.threadIdAndLimitToTakeRecord(thread_id,
                                                      start, length)
        return result
    
    def getThreadName(self, thread_id):
        u'''
        スレッドの名称をスレッドIDより得る
        '''
        result = self.db.getThreadName(thread_id)
        return result[0]
        
    def closeConnect(self):
        u'''
        コネクションを切る
        '''
        self.db.closeConnect()
