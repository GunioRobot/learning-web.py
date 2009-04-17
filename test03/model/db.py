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

    def checkThreadId(self, threadid):
        u'''
        Thread id のカウント
        '''
        query = u'''
                SELECT COUNT(`id`) `count`
                    FROM thread 
                    WHERE thread_id = :thread_id
                '''
        param = {u'thread_id': threadid}
        result = self.fetchAll(query, param)
        return int(result.get(u'count'))

    def newCreateThread(self, args):
        u'''
        threadにレコード追加
        '''
        query = u'''
                INSERT INTO thread 
                     (title, make_time, update_time)
                     VALUES 
                     (:title, NOW(), NOW())
                '''
        param = {u'title': args.get('threadtitle')}
        result = self.insertRecord(query, param)
        if result:
            # 正常に終了した場合は、最後に挿入した行番号を返す
            return self.cur.lastrowid
        else:
            # 異常終了時はFalse
            return False
 
        
    def newCreateRes(self, args):
        u'''
        res にレコード追加
        '''
        query = u'''
                INSERT INTO res
                    (thread_id, name, message, create_time)
                    VALUES
                    (:thread_id, :name, :message, NOW())
                '''
        param = {u'thread_id' : args.get(u'thread_id'),
                 u'name' : args.get(u'username'),
                 u'message': args.get(u'message')}

        result = self.insertRecord(query, param)
        if result:
            # 正常に終了した場合は、最後に挿入した行番号を返す
            return self.cur.lastrowid
        else:
            # 異常終了時はFalse
            return False

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

    def catchResAllRecord(self, thread_id):
        u'''
        res テーブルの全てのレコードを返す
        '''
        query = u'''
                SELECT * FROM res WHERE thread_id = :thread_id
                '''
        param = {u'thread_id': thread_id}
        result = self.fetchAll(query, param)
        return result

    def catchResRecord(self, thread_id, limit, count):
        u'''
        res テーブルの一部のレコードを返す
        '''

        query = u'''
                SELECT * FROM res WHERE thread_id = :thread_id
                         LIMIT :limit,:count
                '''
        param = {u'thread_id': thread_id,
                 u'limit': limit,
                 u'count': count}
        result = self.fetchAll(query, param)
        return result
     
