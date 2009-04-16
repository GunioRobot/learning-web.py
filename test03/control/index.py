#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import web
from model import *

class index(object):
    def GET(self):
        db = dbControl()
        threadrecord = db.catchThreadAllRecord()
        web.header(u'Content-Type', u'text/html')
        render = web.template.render(u'../templates')
        return render.index(u'BBSテスト', threadrecord)
    def POST(self):
        web.seeother(u'/')
