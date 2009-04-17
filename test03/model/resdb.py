#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import db

class resDb(db.dbControl):
    u'''
    レスがらみのDB処理用
    res
    '''
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
