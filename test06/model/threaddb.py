# -*- coding:utf-8 -*-

__version__ = u'200904231811'

import database

class threaddatabase(database.database):
    def takeRecordAll(self):
        u'''
        すべてのレコードを取得
        '''
        query = u'''
                SELECT * FROM thread
                  ORDER BY create_time DESC
                '''
        result = self.fetchAll(query)
        return result
    
    def threadIdToTakeRecord(self, thread_id):
        u'''
        スレッドIDを元に、レコードを取得
        '''
        query = u'''
                SELECT * FROM thread
                  WHERE id = :thread_id
                  ORDER BY create_time DESC
                '''
        param = {u'thread_id' : thread_id}
        result = self.fetchAll(query, param)
        return result
    
    def bbsIdToTakeRecord(self, bbs_id):
        u'''
        bbsidを元に、レコードを取得
        '''
        query = u''' 
                SELECT * FROM thread
                  WHERE bbs_id = :bbs_id
                '''
        param = {u'bbs_id' : bbs_id}
        result = self.fetchAll(query, param)
        return result
    
