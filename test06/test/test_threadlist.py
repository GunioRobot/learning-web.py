#!/usr/local/bin/python
# -*- coding:utf-8 -*-

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
        condb = threadlist.threadlist(TEST_DBNAME)
        result = condb.takeThreadList()
        self.assertEqual(result[0][1], 2)
        self.assertEqual(result[1][2], u'テストスレッドPart2')

def suite():
    u'''
    テストケースの登録
    '''
    test = [u'test_takeThreadList']
    return unittest.TestSuite(map(TestThreadList, test))

if __name__ == u'__main__':
    createTestDataBase()
    unittest.TextTestRunner(verbosity=2).run(suite())
