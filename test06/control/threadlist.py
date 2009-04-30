# -*- coding:utf-8 -*-

u'''
スレッドに関する処理
'''


import web
import os
import sys

from model import threaddb
from config import conf

class threadlist(object):
    u'''
    スレッドに関する処理
    '''
    def __init__(self, dbname=conf.DATABASE_PATH):
        u'''
        コンストラクタ
        '''
        self.db = threaddb.threaddatabase(dbname)
    
    def takeThreadList(self):
        u'''
        スレッドすべてのレコードを取得する
        '''
        result = self.db.takeRecordAll()
        return result

    def takeThreadIdToTakeRecord(self, thread_id):
        u'''
        スレッドIDを元にスレッドのレコードを求める
        '''
        result = self.db.threadIdToTakeRecord(thread_id)
        return result

    def takebbsIdToTakeRecord(self, bbs_id):
        u'''
        bbsIDを元にスレッドのレコードを求める
        '''
        result = self.db.bbsIdToTakeRecord(bbs_id)
        return result

    def closeConnect(self):
        u'''
        コネクションを切る
        '''
        self.db.closeConnect()
