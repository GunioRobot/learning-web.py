# -*- coding:utf-8 -*-

__version__ = u'200904231811'

import database

class threaddatabase(database.database):
    u'''
    作成されているスレッド全体に関する処理
    '''
    
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
        
    def newThreadInsertToRecord(self, bbs_id, threadtitle):
        u'''
        スレッド新規作成時のために
        レコードにスレッドの情報を入力する
        bbs_id threadtitle をレコードに追加する
        bbs_idが一致しなければ、処理は行わない
        挿入後は、問題ない場合は挿入した行数を返す
        '''
        if self.checkBbsId(bbs_id) == 0:
            return False
            
        query = u'''
                INSERT INTO thread
                  (bbs_id, name, create_time)
                  VALUES
                  (:bbs_id, :name, NOW())
                '''
        param = {u'bbs_id' : bbs_id,
                 u'name' : threadtitle}
        result = self.sendQuery(query, param)
        if result:
            return self.getLastRowId()
        else:
            return False
        
    def checkBbsId(self, bbs_id):
        u'''
        指定されたbbs_idについてカウントし、結果を返す
        '''
        query = u'''
                SELECT count(id) `count` 
                  FROM thread 
                  WHERE bbs_id = :bbs_id
                  LIMIT 1
                '''
        param = {u'bbs_id' : bbs_id}
        result = self.fetchOne(query, param)
        return result[0]
    
    def getThreadName(self, thread_id):
        u'''
        スレッドIDを元に、スレッド名を求め、返す
        '''
        query = u'''
                SELECT name 
                   FROM thread
                   WHERE id = :thread_id
                   LIMIT 1
                '''
        param = {u'thread_id' : thread_id}
        result = self.fetchOne(query, param)
        return result
   
