# -*- coding: utf-8 -*-

__version__ = u'200904211354'

import database

class bbsdatabase(database.database):
    def takeRecordAll(self):
        query = u'''
                SELECT * FROM bbs
                '''
        result = self.fetchAll(query)
        return result

    def bbsIdToTakeRecord(self, bbs_id):
        query = u'''
                SELECT * FROM bbs
                  WHERE id = :bbs_id
                '''
        param = {u'bbs_id' : bbs_id}
        result = self.fetchAll(query, param)
        return result

    def categoryIdToTakeRecord(self, category_id):
        query = u'''
                SELECT * FROM bbs
                  WHERE category_id = :category_id
                '''
        param = {u'category_id' : category_id}
        result = self.fetchAll(query, param)
        return result
