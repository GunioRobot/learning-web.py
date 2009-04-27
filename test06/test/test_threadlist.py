#!/usr/local/bin/python
# -*- coding:utf-8 -*-

u'''
control.threadlist について確認
'''

import unittest
import os
import sys
if not os.path.abspath(u'../') in sys.path:
    sys.path.append(os.path.abspath(u'../'))

from control import threadlist
from setup import setupdb
from create_testdatabase import *

class TestThreadList(unittest.TestCase):
    u'''
    control.threadlist.threadlist についてテスト
    '''
    def test_takeThreadList(self):
        u'''
        takeThreadListについてテスト
        '''
        condb = threadlist.threadlist(TEST_DBNAME)
        result = condb.takeThreadList()
        
        self.assertEqual(result[0][1], 2)
        self.assertEqual(result[1][2], u'テストスレッドPart2')
        
        condb.closeConnect()
        
    def test_takeThreadIdToTakeRecord(self):
        u'''
        takeThreadIdToTakeRecordについてテスト
        '''
        condb = threadlist.threadlist(TEST_DBNAME)
        result = condb.takeThreadIdToTakeRecord(2)
        
        self.assertEqual(result[0][1], 1)
        self.assertEqual(result[0][2], u'テストスレッドPart2')
        
        condb.closeConnect()
        
    def test_takebbsIdToTakeRecord(self):
        u'''
        takebbsIdToTakeRecordについてテスト
        '''
        condb = threadlist.threadlist(TEST_DBNAME)
        result = condb.takebbsIdToTakeRecord(2)
        
        self.assertEqual(result[0][1], 2)
        self.assertEqual(result[0][2], u'ほげほげ板にようこそ')
        
        condb.closeConnect()
        
        

def suite():
    u'''
    テストケースの登録
    '''
    test = [u'test_takeThreadList', u'test_takeThreadIdToTakeRecord',
            u'test_takebbsIdToTakeRecord']
    return unittest.TestSuite(map(TestThreadList, test))

if __name__ == u'__main__':
    createTestDataBase()
    unittest.TextTestRunner(verbosity=2).run(suite())
