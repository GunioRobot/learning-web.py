# -*- coding:utf-8 -*-

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
        self.db = threaddb.threaddatabase(dbname)
    
    def takeThreadList(self):
        result = self.db.takeRecordAll()
        return result

    def takeThreadIdToTakeRecord(self, thread_id):
        result = self.db.threadIdToTakeRecord(thread_id)
        return result

    def takebbsIdToTakeRecord(self, bbs_id):
        result = self.db.bbsIdToTakeRecord(bbs_id)
        return result

    def closeConnect(self):
        u'''
        コネクションを切る
        '''
        self.db.closeConnect()
