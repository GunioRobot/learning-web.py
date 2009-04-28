# -*- coding:utf-8 -*-

u'''
新規にスレッドを作成する
'''

from model import insertnewthread
from config import conf

class newthread(object):
    def __init__(self, dbname=conf.DATABASE_PATH):
        u'''
        コンストラクタ
        '''
        self.db = insertnewthread.insertnewthread(dbname)
    
    def newThread(self, bbs_id, threadtitle, username, message):
        u'''
        スレッド作成を行う
        成功した場合はTrueを返す
        '''
        threadlastrowid = self.db.newThreadInsertToRecord(bbs_id,
                                                          threadtitle)
        if threadlastrowid is False:
            self.db.rollback()
            self.db.closeConnect()
            return False
            
        reslastrowid = self.db.newResToThreadId(threadlastrowid,
                                                username, message)
        
        if reslastrowid is False:
            self.db.rollback()
            self.db.closeConnect()
            return False

        self.db.commit()
        self.db.closeConnect()
        
        return True