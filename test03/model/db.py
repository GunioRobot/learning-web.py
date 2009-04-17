#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import time

DATABASE = u'../datastore/bbs.db'

class dbControl(object):
    def __init__(self, database=DATABASE):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
        self.addNow()
  
    def addNow(self):
        u'''
        NOW関数を追加する
        '''
        def NOW():
	    now = time.localtime()
	    return (str(now.tm_year)+ '-' +
		    str(now.tm_mon).zfill(2) + '-' +
		    str(now.tm_mday).zfill(2) + ' ' +
		    str(now.tm_hour).zfill(2) + ':' +
		    str(now.tm_min).zfill(2) + ':' +
		    str(now.tm_sec).zfill(2))

        self.con.create_function('NOW', 0, NOW)
    
    def fetchAll(self, query, param=None):
        u'''
        SELECT
        '''
        try:
            if param:
                self.cur.execute(query, param)
            else:
                self.cur.execute(query)
        except sqlite3.Error, e:
            for x in e.args:
                print(x)

        return self.cur.fetchall()

    def commit(self):
        self.con.commit()
    def rollback(self):
        self.con.rollback()
    def close(self):
        self.cur.close()
        self.con.close()
  
    def insertRecord(self, query, param=None):
        u'''
        レコード更新
        '''
        try:
            if param:
                self.cur.execute(query, param)
            else:
                self.cur.execute(query)
        except sqlite3.Error, e:
            for x in e.args:
                print(x)
            return False

        return True     
