# -*- coding:utf-8 -*-

import web
import time
import re

from control.threadlist import threadlist

class bbs(object):
    def __init__(self):
        self.render = web.template.Render(u'../templates')
    def GET(self):
        u'''
        BBSが持っているスレッド一覧を表示する
        '''
        # bbsidの取得
        data = web.webapi.input()
        if (data.get(u'no') and
            re.match(ur'^[0-9]{1,10}$', data.get(u'no'))):
            db = threadlist()
            tlist = db.takebbsIdToTakeRecord(data.get(u'no'))
            return self.render.thread(tlist)
        else:
            web.seeother(u'/')
            return

    def POST(self):
        web.seeother(u'/')
