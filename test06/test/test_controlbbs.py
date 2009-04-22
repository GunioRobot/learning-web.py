#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import unittest
import os
import sys
if not os.path.abspath(u'../') in sys.path:
    sys.path.append(os.path.abspath(u'../'))

from control import controlbbs
from setup import setupdb

class TestControlBbs(unittest.TestCase):


    def setUp(self):
        self.condb = controlbbs.controlbbs(u':memory:')
        query = setupdb.CREATE_TABLE
        self.condb.db.executeScript(query)
        query = u'''
                INSERT INTO category
                  (name) 
                  VALUES
                  ('category_1');

                INSERT INTO bbs
                  (category_id, name, create_time)
                  VALUES
                  (1, 'testbbs_1', '2009-04-01 00:00:00');

                INSERT INTO thread
                  (bbs_id, name, create_time)
                  VALUES
                  (1, 'test_thread_1', '2009-04-02 11:12:12');
              
                INSERT INTO res
                  (thread_id, user_name, message, create_time, update_time)
                  VALUES
                  (1, 'testuser', 'testmessage', '2009-04-04 00:00:00',
                   '2009-04-05 11:11:11');
                '''
        self.condb.db.executeScript(query)
    
    def test_takeBbsList(self):
        u'''
        takeBbsListのテスト
        '''
        db = self.condb.takeBbsList()
        self.assertEqual(1, db[0][1]) # category_idの確認
        self.assertEqual(u'testbbs_1', db[0][2]) # bbs名の確認


if __name__ == u'__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestControlBbs)
    #unittest.TextTestRunner(verbosity=2).run(suite)
            
