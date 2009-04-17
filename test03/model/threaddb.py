#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import db

class threadDb(db.dbControl):
    u'''
    スレッドがらみのDB処理用
    thread
    '''
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
