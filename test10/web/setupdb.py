#!/usr/local/bin/python
# -*- coding:utf-8 -*-

u'''
マイグレーション用ファイル
'''

import sqlite3
import os
import sys

def setup():
    if not os.path.exists(u'../db'):
        os.mkdir(u'../db', 0755)

    if os.path.exists(u'../db/files.db'):
        os.unlink(u'../db/files.db')

    query = u'''
            CREATE TABLE files (
              id INTEGER NOT NULL PRIMARY KEY,
              name TEXT NOT NULL,
              size REAL NOT NULL,
              comment TEXT,
              uploadtime TEXT NOT NULL,
              addr TEXT NOT NULL
            );
   
            CREATE TABLE downsession(
              id INTEGER NOT NULL PRIMARY KEY,
              session TEXT NOT NULL,
              expiretime TEXT NOT NULL,
              inserttime TEXT NOT NULL
            );
            '''
    try:
        con = sqlite3.connect(u'../db/files.db')
        con.executescript(query)
    except sqlite3.Error, e:
        for i in e.args:
            print(i)
        print(u"DB Error")
        con.close()
        sys.exit(1)

    con.commit()
    con.close()
    os.chmod(u'../db/files.db', 0660)

    print(u'done.')

if __name__ == u'__main__':
    setup()
