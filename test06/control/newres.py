# -*- coding:utf-8 -*-

u'''
レス作成時に利用する
'''

from model import resdb
from config import conf

class newres(object):
    u'''
    レス作成時に利用
    '''
    def __init__(self, dbname=conf.DATABASE_PATH):
        self.db = resdb.resdatabase(dbname)
        
    def newRes(self, thread_id, username, message):
        u'''
        新規レスの追加
        '''
        result = self.db.newResToThreadId(thread_id, username, message)
        if result:
            self.db.commit()
            return True
        else:
            self.db.rollBack()
            return False