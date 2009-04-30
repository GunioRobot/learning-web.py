# -*- coding: utf-8 -*-

__version__ = u'200904211354'

import database

class bbsdatabase(database.database):
    u'''
    bbsテーブルにかかわるクラス
    '''
    def takeRecordAll(self):
        u'''
        bbsテーブルすべてのレコードを抜き出す
        '''
        query = u'''
                SELECT * FROM bbs
                  ORDER BY create_time DESC
                '''
        result = self.fetchAll(query)
        return result

    def bbsIdToTakeRecord(self, bbs_id):
        u'''
        主キーを元にレコードを抜き出す
        '''
        query = u'''
                SELECT * FROM bbs
                  WHERE id = :bbs_id
                  ORDER BY create_time DESC
                '''
        param = {u'bbs_id' : bbs_id}
        result = self.fetchAll(query, param)
        return result

    def categoryIdToTakeRecord(self, category_id):
        u'''
        カテゴリーを元にレコードを抜き出す
        '''
        query = u'''
                SELECT * FROM bbs
                  WHERE category_id = :category_id
                  ORDER BY create_time DESC
                '''
        param = {u'category_id' : category_id}
        result = self.fetchAll(query, param)
        return result
