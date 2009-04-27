#!/usr/local/bin/python
# -*- coding:utf-8 -*-

u'''
control.bbslistについて確認
'''

import os
import sys
if not os.path.abspath(u'../') in sys.path:
    sys.path.append(os.path.abspath(u'../'))

from control import bbslist
from setup import setupdb
from create_testdatabase import *

class TestBbsList(unittest.TestCase):
    u'''
    control.bbslist.bbslist についてテスト
    '''
    def test_takeBbsList(self):
        condb = bbslist.bbslist(TEST_DBNAME)
        result = condb.takeBbsList()
        
        self.assertEqual(result[0][1], 1)
        self.assertEqual(result[0][2], u'テストビービーエス')
        
        condb.closeConnect()

    def test_bbsIdTakeBbsList(self):
        condb = bbslist.bbslist(TEST_DBNAME)
        result = condb.bbsIdTakeBbsList(2)
        self.assertEqual(result[0][1], 2)
        self.assertEqual(result[0][2], u'ほげほげ')
        
        condb.closeConnect()

    def test_categoryIdTakeBbsList(self):
        condb = bbslist.bbslist(TEST_DBNAME)
        result = condb.categoryIdTakeBbsList(2)
        
        self.assertEqual(result[0][2], u'ほげほげ')
        self.assertEqual(result[0][3], u'2009-05-05 00:00:00')
        self.assertEqual(result[1][2], u'うげげげ')
        condb.closeConnect()

def suite():
    u'''
    テストケースの登録
    '''
    test = [u'test_takeBbsList', u'test_bbsIdTakeBbsList',
            u'test_categoryIdTakeBbsList']
    return unittest.TestSuite(map(TestBbsList, test))

if __name__ == u'__main__':
    createTestDataBase()
    unittest.TextTestRunner(verbosity=2).run(suite())
            
