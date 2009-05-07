#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web
from klass import *

urls = (
    u'/', u'index',
    u'/upload', u'upload',
    u'/loading', u'loading',
    )

def main():
    u'''
    #メイン関数
    '''
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
