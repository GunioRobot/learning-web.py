#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web
import re

from model import *

class res(object):
    def GET(self):
        usGet = web.webapi.input()
        if (usGet.get(u'no') and
            re.match(ur'^[0-9]+$', usGet.get(u'no'))):
            db = dbControl()
            resrecord = db.catchResAllRecord(usGet.get(u'no'))
            render = web.template.render('../templates')
            return render.res(resrecord)
        else:
            web.seeother(u'/')
    def POST(self):
        pass
