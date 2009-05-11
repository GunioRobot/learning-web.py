#!/usr/local/bin/python2.6
# -*- coding:utf-8 -*-

import web
from klass import *

urls = (
    u'/', u'index',
    u'/upload', u'upload',
    u'/loading', u'loading',
    u'/chkloading', u'chkloading',
    u'/delfile', u'delfile',
    u'/.*', u'index',
    )

def main():
    u'''
    #メイン関数
    '''
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
