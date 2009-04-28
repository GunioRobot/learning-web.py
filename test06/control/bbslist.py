# -*- coding: utf-8 -*-

u'''
BBS一覧を取得する
'''

import web
import os
import sys

from model import bbsdb
from config import conf

class bbslist(object):
    def __init__(self, dbname=conf.DATABASE_PATH):
        u'''
        コンストラクタ
        '''
        self.db = bbsdb.bbsdatabase(dbname)
        
    def takeBbsList(self):
        u'''
        すべてのBBSリストを得る
        '''
        result = self.db.takeRecordAll()
        self.closeConnect()
        return result

    def bbsIdTakeBbsList(self, bbs_id):
        u'''
        BBS IDを元にBBSリストを得る
        '''
        result = self.db.bbsIdToTakeRecord(bbs_id)
        self.closeConnect()
        return result

    def categoryIdTakeBbsList(self, category_id):
        u'''
        CATEGORY IDを元にBBSリストを得る
        '''
        result = self.db.categoryIdToTakeRecord(category_id)
        self.closeConnect()
        return result

    def closeConnect(self):
        u'''
        コネクションを切断
        '''
        self.db.closeConnect()
