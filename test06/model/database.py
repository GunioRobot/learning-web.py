# -*- coding: utf-8 -*-

u'''
DBを実際にいじくる、
そのためのクラスで本家みたいなもん。
'''

import sqlite3
import os
import time

__version__ = u'200904282208'

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
        if (not os.path.exists(dbname) and 
            isinstance(dbname, file)):
            raise self.DataBaseError, dbname

        self.dbname = dbname
        self.openConnect()
        self.makeOriginalDefinition() # NOWとか追加
        self.openCursor()
        
    def makeOriginalDefinition(self):
        u'''
        sqlite3では無いような関数を定義する
        意欲的なメソッド
        '''
        import originaldefinition

        if isinstance(self.con, sqlite3.Connection):
            for item in originaldefinition.funclist:
                self.con.create_function(*item)
        else:
            return False
        

    def openConnect(self):
        u'''
        コネクトする
        '''
        try:
            if (not os.path.exists(self.dbname) and
                isinstance(self.dbname, file)):
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
        try:
            self.con.close()
            return True
        except ProgrammingError, e:
            return False
            
    def getLastRowId(self):
        u'''
        最後にINSERTで挿入した
        レコードの行番号を得て返す
        '''
        return self.cur.lastrowid

    def commit(self):
        u'''
        コミット
        '''
        self.con.commit()
    
    def rollback(self):
        u'''
        ロールバック
        '''
        self.con.rollback()

    def __execute(self, query, param=None):
        u'''
        渡されたクエリ、パラメータについて受け取り、
        カーソルオブジェクトに渡して実行する
        query string
        param dict
        '''
        if self.__class__ == database:
            raise NotImplementedError
        if not param:
            self.cur.execute(query)
        else:
            self.cur.execute(query, param)

    def fetchAll(self, query, param=None):
        u'''
        execute後、カーソルのfetchallメソッドを呼び、
        クエリの条件にあうレコードすべて取り出す
        '''
        self.__execute(query, param)
        return self.cur.fetchall()

    def fetchOne(self, query, param=None):
        u'''
        execute後、カーソルのfetchoneメソッドを呼び、
        クエリの条件にあうレコードの一行目のものについて
        取り出す
        '''
        self.__execute(query, param)
        return self.cur.fetchone()
 
    def sendQuery(self, query, param=None):
        u'''
        execute後、ただTrueを返す。
        INSERT, UPDATE実行用メソッド
        '''
        self.__execute(query, param)
        return True

    def executeScript(self, query):
        u'''
        executescriptメソッドを利用。
        複数行にわたるクエリを実行するのに利用する
        '''
        self.cur.executescript(query)
        return True
