# -*- coding:utf-8 -*-

u'''
resdbのテスト
'''

import unittest
import os
import sys
if not os.path.abspath(u'../') in sys.path:
    sys.path.append(os.path.abspath(u'../'))

from control import  thread
from setup import setupdb
from create_testdatabase import *

class TestResDb(unittest.TestCase):

    def test_threadIdToTakeRecord(self):
        u'''
        スレッドIDでの指定引きテスト
        '''
        condb = thread.thread(TEST_DBNAME)
        result = condb.threadIdToTakeRecord(1)
        self.assertEqual(result[0][2], u'てすとゆーざ')
        
    def test_threadIdAndLimitToTakeRecord(self):
        u'''
        スレッドIDかつ
        範囲指定時のテスト
        '''
        condb = thread.thread(TEST_DBNAME)
        result = condb.threadIdAndLimitToTakeRecord(1,2,2)
        self.assertEqual(result[0][2], u'うげげ')
        self.assertEqual(result[1][3], u'メッセージテスト')
    
    def test_getThreadName(self):
        u'''
        スレッドIDの取得テスト
        '''
        condb = thread.thread(TEST_DBNAME)
        result = condb.getThreadName(3)
        self.assertEqual(result, u'ほげほげ板にようこそ')
        
def suite():
    u'''
    テストスイート作成
    '''
    test = [u'test_threadIdToTakeRecord',
            u'test_threadIdAndLimitToTakeRecord',
            u'test_getThreadName']
    return unittest.TestSuite(map(TestResDb, test))

if __name__ == u'__main__':
    createTestDataBase()
    unittest.TextTestRunner(verbosity=2).run(suite())
    
