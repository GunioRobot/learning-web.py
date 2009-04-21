# -*- coding: utf-8 -*-

import sqlite3
import os
import time

__version__ = u'200904211236'

class database(object):
    u'''
    con コネクト
    cur カーソルオブジェクトを格納するディクショナリ
    '''
    class DataBaseError(BaseException):
        u'''
        DataBaseError
        '''
        pass

    def __init__(self, dbname):
        u'''
        コンストラクタ
        '''
        print dbname
        if not os.path.exists(dbname):
            raise self.DataBaseError, dbname

        self.dbname = dbname
        self.openConnect()
        self.openCursor()

    def openConnect(self):
        u'''
        コネクトする
        '''
        try:
            if not os.path.exists(self.dbname):
                return False
            if isinstance(self.con, sqlite3.Conenct):
                return False
        except AttributeError, e:
            self.con = sqlite3.connect(self.dbname)            
        except sqlite3.Error, e:
            raise self.DataBaseError, u'DB Error'

    def openCursor(self):
        u'''
        カーソルを開く
        '''
        try:
            if isinstance(self.cur, sqlite3.Cursor):
                return False
        except AttributeError, e:
            self.cur = self.con.cursor()
        except sqlite3.Error, e:
            raise self.DataBaseError, u'DB Error'
        
    def closeCursor(self):
        u'''
        カーソルを閉じる
        '''
        self.cur.close()

    def closeConnect(self):
        u'''
        接続を閉じる
        '''
        self.con.close()

    def commit(self):
        self.con.commit()
    
    def rollback(self):
        self.con.rollback()

    def __execute(self, query, param=None):
        if self.__class__ == database:
            raise NotImplementedError
        if not param:
            self.cur.execute(query)
        else:
            self.cur.execute(query, param)

    def fetchAll(self, query, param=None):
        self.__execute(query, param)
        return self.cur.fetchall()

    def fetchOne(self, query, param=None):
        self.__execute(query,param)
        return self.cur.fetchone()

