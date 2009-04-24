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
        result = self.db.findAll(query, param)
        return result
