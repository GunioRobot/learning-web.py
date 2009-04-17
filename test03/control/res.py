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
            web.header(u'Content-Type', u'text/html')
            return render.res(resrecord, u'/res?no={0}'.format(usGet.get(u'no')))
        else:
            web.seeother(u'/')
    def POST(self):
        usGet = web.webapi.input()
        if (usGet.get(u'username') and
            usGet.get(u'message')):
            db = dbControl()
            # レスデータをレコードに書き込む
            post = {u'thread_id': usGet.get(u'no'),
                    u'username' : usGet.get(u'username'),
                    u'message' : usGet.get(u'message')}
            result = db.newCreateRes(post)
            if not result:
                db.rollback()
                db.close()
                web.seeother(u'/error')
            else:
                db.commit()
                web.seeother(u'/res?no={0}'.format(usGet.get(u'no')))
        else:
            web.seeother(u'/')
