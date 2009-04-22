#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

DATASTORE_DIR = u'../datastore/'
DATABASE_NAME = u'bbs.db'

__version__ = u'200904202327'

CREATE_TABLE = \
u'''
CREATE TABLE category(
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE bbs (
  id INTEGER NOT NULL PRIMARY KEY,
  category_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  create_time TEXT NOT NULL
);

CREATE TABLE thread(
  id INTEGER NOT NULL PRIMARY KEY,
  bbs_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  create_time TEXT NOT NULL
);

CREATE TABLE res(
  id INTEGER NOT NULL PRIMARY KEY,
  thread_id INTEGER NOT NULL,
  user_name TEXT NOT NULL,
  message TEXT NOT NULL,
  create_time TEXT NOT NULL,
  update_time TEXT NOT NULL
);

CREATE INDEX idx_bbs_category_id ON bbs(category_id);
CREATE INDEX idx_thread_bbs_id ON thread(bbs_id);
CREATE INDEX idx_res_thread_id ON res(thread_id);
'''



def setupDb():
    u'''
    DBファイルの作成
    '''
    if os.path.exists(os.path.join(DATASTORE_DIR, DATABASE_NAME)):
        while True:
            print(u'Deleted DATABASE? y/n')
            ch = raw_input()
            if ch in ['y','Y']:
                os.unlink(os.path.join(DATASTORE_DIR, DATABASE_NAME))
                break

    con = sqlite3.connect(os.path.join(DATASTORE_DIR, DATABASE_NAME))
    cur = con.cursor()
   
    try:
        cur.executescript(CREATE_TABLE)
    except sqlite3.Error, e:
        cur.rollback()
        for i in e.args:
            print(i)
        print(u'Error!')
        sys.exit(1)
    
    con.commit()
    con.close()

    print(u'done.')
    

if __name__ == u'__main__':
    setupDb()
