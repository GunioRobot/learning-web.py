#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

__version__ = '200904161807'

DATABASE = 'datastore/bbs.db'

QUERY_1 = \
'''
CREATE TABLE `thread` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `title` TEXT NOT NULL,
  `make_time` TEXT NOT NULL,
  `update_time` TEXT NOT NULL,
  UNIQUE(`title`)
)
'''

QUERY_2 = \
'''
CREATE TABLE `res`(
  `id` INTEGER NOT NULL PRIMARY KEY,
  `thread_id` INTEGER NOT NULL,
  `name` TEXT NOT NULL,
  `message` TEXT NOT NULL,
  `create_time` TEXT NOT NULL
)
'''

QUERY_3 = \
'''
CREATE INDEX t_key ON thread(title)
'''

QUERY_4 = \
'''
CREATE INDEX tid_key ON res(thread_id)
'''

QUERY_LIST = [QUERY_1, QUERY_2, QUERY_3, QUERY_4]

def setupDb(database=DATABASE, tablelist=QUERY_LIST):
    if os.path.exists(database):
        s = None
        while not s in ['n','N','y','Y']:
            print('IS {0} deleted?'.format(database))
            s = raw_input()

            if s in ['y','Y']:
                os.unlink(database)
                print('\nDelete {0}.'.format(database))
            else:
                print('\nNothing is done.')
                sys.exit(1)
   
    try:     
        db = sqlite3.connect(database)
        cur = db.cursor()
        for table in tablelist:
            cur.execute(table)
            print(table)
            
    except sqlite3.Error, e:
        db.rollback()
        for x in e.args:
            print(x)
        print('\nDB ERROR!')
        cur.close()
        db.close()
        sys.exit(1)

    db.commit()
    cur.close()
    db.close()

    print('done.')

if __name__ == '__main__':
    setupDb()
