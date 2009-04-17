#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web

class error(object):
    def GET(self):
        web.header(u'Content-Type', u'text/html')
        return u'エラーが発生しました。'
    def POST(self):
        web.seeother(u'/')
