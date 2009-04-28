# -*- coding:utf-8 -*-

import web
import time

from control.bbslist import bbslist

class bbsindex(object):
    def __init__(self):
        self.render = web.template.Render(u'../templates')
    def GET(self):
        u'''
        すべてのBBSリストを得てテンプレートに反映する
        '''
        conbbs = bbslist()
        blist = conbbs.takeBbsList()
        web.header(u'Content-Type', u'text/html; charset=UTF-8')
        return self.render.bbs(blist)
        
    def POST(self):
        web.seeother(u'/')
