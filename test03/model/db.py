#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3

DATABASE = u'datastore/bbs.db'

class dbControl(object):
    def __init__(self, database=DATABASE):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
    
    def fetchAll(self, query, param=None):
        try:
            if param:
                self.cur.execute(query, param)
            else:
                self.cur.execute(query)
        except sqlite3.Error, e:
            for x in e.args:
                print(x)

        return self.cur.fetchall()

    def catchThreadAllRecord(self):
        u'''
        thread テーブルの全てのレコードを返す
        '''
        query = u'''
                SELECT * FROM thread
                '''
        result = self.fetchAll(query)
        return result
    
    def catchThreadRecord(self, limit, count):
        u'''
        thread テーブルについて、一部のレコードを取得する
        '''
        query = u'''
                SELECT * FROM thread LIMIT :limit,:count
                '''
        param = {u'limit':limit, u'count':count}

    def catchResAllRecord(self):
        u'''
        res テーブルの全てのレコードを返す
        '''
        query = u'''
                SELECT * FROM res
                '''
        result = self.fetchAll(query)
        return result

    def catchResRecord(self, limit, count):
        
     
