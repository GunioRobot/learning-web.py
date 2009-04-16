#!/opt/local/bin/python2.6
# -*- coding: utf-8 -*-

import web
import sqlite3
import sys
import re

urls = (
    u'/', u'index',
    u'/insert', u'insert',
    u'/.*', u'redirect' )

DBFILE = u'bbs.db'
PAGE = 10

class bbs(object):
    u'''
    掲示板クラス。テーブルにレコードを挿入したり、
    取得したり。
    '''
    def __init__(self):
        u'''
        コンストラクタ
        '''
        self.con = sqlite3.connect(DBFILE)
        self.cur = self.con.cursor()

    def catchRecord(self, min, max):
        u'''
        bbsのデータを手に入れる。
        結果、無い場合は空配列が戻る。
        min 取得開始行
        max 取得終了行
        '''
        query = u'''
                SELECT * FROM bbs LIMIT :min,:max
                '''
        param = {u'min':min, u'max':max}
        try:
            self.cur.execute(query, param)
            result = self.cur.fetchall()
        except sqlite3.error, e:
            for i in e.args:
                print i
            sys.exit(1)
        
        return result
        
    def insertRecord(self, name, message):
        u'''
        DBにデータを挿入する
        '''
        query = u'''
                INSERT INTO bbs 
                  (name, message) 
                VALUES
                  (:name, :message)
                '''
        param = {u'name':name, u'message':message}
        try:
            self.cur.execute(query,param)
        except sqlite3.error, e:
            self.con.rollback()
            for i in e.args:
                print i
            sys.exit(1)

        self.con.commit()

    def countRows(self):
        u'''
        レコードの行数をカウントする
        '''
        query = u'SELECT count(`id`) `count` FROM `bbs`'
        try:
            self.cur.execute(query)
            result = self.cur.fetchone()
        except sqlite3, e:
            for i in e.args:
                print i
            sys.exit(1)

        return int(result[0])
        
    def closeCursor(self):
        self.cur.close()

    def closeConnect(self):
        self.con.close()

if __name__ == u'__main__':
    app = web.application(urls, globals())
    app.run()
