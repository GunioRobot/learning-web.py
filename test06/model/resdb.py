# -*- coding:utf-8 -*-

__version__ = u'200904241203'

import database

class resdatabase(database.database):
    def takeRecordAll(self):
        u'''
        すべてのレコードを取得
        '''
        query = u'''
                SELECT * FROM res
                  ORDER BY update_time DESC 
                '''
        result = self.fetchAll(query)
        return result
    def threadIdToTakeRecord(self, thread_id):
        u'''
        スレッドIDを元にレコードを取る
        '''
        query = u'''
                SELECT * FROM res
                  WHERE thread_id = :thread_id
                  ORDER BY update_time DESC
                '''
        param = {u'thread_id' : thread_id}
        result = self.fetchAll(query, param)
        return result

    def threadIdAndLimitToTakeRecord(self, thread_id,
                                     start, length):
        u'''
        スレッドID, LIMITを指定する
        '''
        query = u'''
                SELECT * FROM res
                  WHERE thread_id = :thread_id
                  ORDER BY update_time DESC
                  LIMIT start, length
                '''
        param = {u'thread_id' : thread_id,
                 u'start' : start,
                 u'length' : length}
        result = self.fetchAll(query, param)
        return result
        
    def newResToThreadId(self, thread_id,
                           user_name, message):
        u'''
        新レスを作成する
        スレッドIDが存在しない場合は処理しない
        挿入後は、問題ない場合は挿入した行数を返す
        '''
        if self.checkThreadId(thread_id) == 0:
            return False
        query = u'''
                INSERT INTO res
                  (thread_id, user_name, message, create_time, update_time)
                  VALUES
                  (:thread_id, :user_name, :message, NOW(), NOW())
                '''
        param = {u'thread_id' : thread_id,
                 u'user_name' : user_name,
                 u'message' : message}
        result = self.sendQuery(query, param)
        if result:
            return self.getLastRowId()
        else:
            return False
        
    def checkThreadId(self, thread_id):
        u'''
        スレッドIDの有無確認
        '''
        query = u'''
                SELECT count(id) `count`
                  FROM thread
                  WHERE id = :thread_id
                '''
        param = {u'thread_id' : thread_id}
        result = self.fetchOne(query, param)
        return result[0]

