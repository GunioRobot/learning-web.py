#!/opt/local/bin/python2.6
# -*- coding: utf-8 -*-

import sqlite3
import sys

VERSION = u'200904140248'
DBFILE = u'bbs.db'

def createBbsDb():
    u'''
    データベースファイルの作成。
    掲示板テスト用途。
    '''
    con = sqlite3.connect(DBFILE)
    cur = con.cursor()
    try:
        query = u'''
                CREATE TABLE bbs (
                  id INTEGER NOT NULL PRIMARY KEY,
                  name TEXT,
                  message TEXT
                )
                '''
        cur.execute(query)
        con.commit()
    except sqlite3.error, e:
        con.rollback()
        for i in e.args:
            print i
        sys.exit(1)

    cur.close()
    con.close()
    print u'done.'

if __name__ == u'__main__':
    createBbsDb()
