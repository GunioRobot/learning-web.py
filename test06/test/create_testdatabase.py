#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import os
import sys
if not os.path.abspath(u'../') in sys.path:
    sys.path.append(os.path.abspath(u'../'))

from setup import setupdb

TEST_DBNAME = u'test.db'

INSERT_RECORD = \
u'''
INSERT INTO category
  (name)
  VALUES
  ('テストカテゴリー1');

INSERT INTO category
  (name)
  VALUES
  ('テストカテゴリー2');

INSERT INTO bbs
  (category_id, name, create_time)
  VALUES
  (1, 'テストビービーエス', '2009-04-01 00:00:00');

INSERT INTO bbs
  (category_id, name, create_time)
  VALUES
  (2, 'ほげほげ', '2009-05-05 00:00:00');

INSERT INTO bbs
  (category_id, name, create_time)
  VALUES
  (2, 'うげげげ', '2009-05-06 10:00:00');

INSERT INTO thread
  (bbs_id, name, create_time)
  VALUES
  (1, 'テストすれっど', '2009-04-02 01:00:00');

INSERT INTO thread
  (bbs_id, name, create_time)
  VALUES
  (1, 'テストスレッドPart2', '2009-04-02 07:00:00');

INSERT INTO thread
  (bbs_id, name, create_time)
  VALUES
  (2, 'ほげほげ板にようこそ', '2009-04-02 08:00:00');

INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (1, 'てすとゆーざ', 'てすとですよ、僕のメッセージ\n', 
   '2009-04-04 00:00:00', '2009-04-04 01:00:00');

INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (1, 'ほげほげ', 'ほげほげテスト',
   '2009-04-10 00:00:00', '2009-04-12 00:10:00');
   
INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (1, 'うげげ', '変態メッセージテスト',
   '2009-04-12 10:00:00', '2009-04-12 10:00:00');

INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (1, 'どどどど', 'メッセージテスト',
   '2009-04-13 00:00:00', '2009-04-14 00:00:00');

INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (2, 'テストテスト', 'テストですね\nよかったです',
   '2009-06-01 00:00:00', '2009-06-02 00:00:00');

INSERT INTO res
  (thread_id, user_name, message, create_time, update_time)
  VALUES
  (3, 'ほげほげ用テスト', 'ほげほげほげほげ\n',
   '2009-06-06 10:00:00', '2009-07-01 00:00:00');
'''

def createTestDataBase():
    u'''
    テストDBを作成する
    '''
    if os.path.exists(TEST_DBNAME):
        os.unlink(TEST_DBNAME)
    db = sqlite3.connect(TEST_DBNAME)
    db.executescript(setupdb.CREATE_TABLE)
    db.executescript(INSERT_RECORD)
    db.commit()
    db.close()

