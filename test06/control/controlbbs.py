# -*- coding: utf-8 -*-

import web
import os
import sys

from model import bbsdb
from config import conf

class controlbbs(object):
    def __init__(self, dbname=conf.DATABASE_PATH):
        self.db = bbsdb.bbsdatabase(dbname)
        
    def takeBbsList(self):
        u'''
        すべてのBBSリストを得る
        '''
        result = self.db.takeRecordAll()
        return result

    def bbsIdTakeBbsList(self, bbs_id):
        u'''
        BBS IDを元にBBSリストを得る
        '''
        result = self.db.bbsIdToTakeRecord(bbs_id)
        return result

    def categoryIdTakeBbsList(self, category_id):
        u'''
        CATEGORY IDを元にBBSリストを得る
        '''
        result = self.db.categoryIdToTakeRecord(category_id)
        return result
