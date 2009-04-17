#!/usr/local/bin/python2.6
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

import query

__version__ = '200904171905'

DBFILE = u'../datastore/bbs.db'

def setupDataBase(dbfile=DBFILE):
    if os.path.exists(dbfile):
        print(u'May {0} is deleted? y/n'.format(dbfile))
        x = ''
        while not x:
            x = raw_input()
            if not x in [u'y',u'Y',u'n',u'N']:
                x = ''
            elif x in [u'y', u'Y']:
                os.unlink(dbfile)
            elif x in [u'n', u'N']:
                print(u'Stop.')
                return

    try:
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        cur.executescript(query.SETUP_QUERY)
    except sqlite3.Error, e:
        for x in e.args:
            print(x)
        con.rollback()
        print(u'DB Error')
    con.commit()
    con.close()

    print(u'Done.')

if __name__ == '__main__':
    setupDataBase()
