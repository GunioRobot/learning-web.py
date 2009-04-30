# -*- coding:utf-8 -*-

# スレッドの内容を表示する

import web
import time
import re

from control.thread import thread
from config import conf

class threadres(object):
    def __init__(self):
        self.db = thread()
        self.render = web.template.Render(u'../templates')
        
    def GET(self):
        u'''
        GET
        '''
        web.header(u'Content-Type', u'text/html; charset=UTF-8')
        self.setWebInput()
        self.setThreadId(self.mixed.get(u'no'))
        if self.getNo():
            return self.returnRes()
        else:
            web.seeother(u'/')

    def POST(self):
        u'''
        POST
        '''
        web.seeother(u'/')
                

    def setWebInput(self):
        u'''
        web.webapi.input()よりGET, POSTを得る
        '''
        self.mixed = web.webapi.input()
 
    def getRe(self, key, restring):
        u'''
        キー取得
        '''
        if (self.mixed.get(key) and
            re.match(restring, self.mixed.get(key))):
            return self.mixed.get(key)
        else:
            return False

    def getNo(self):
        u'''
        no を取得
        '''
        return self.getRe(u'no', ur'^[0-9]{1,10}$')

    def getStart(self):
        u'''
        start を取得
        '''
        return self.getRe(u'start', ur'^[0-9]{1,3}$')

    def getLength(self):
        u'''
        length を取得
        '''
        return self.getRe(u'length', ur'^[0-9]{1,3}$')

    def setThreadId(self, tid):
        u'''
        threadid のセッター
        '''
        self.thread_id = tid

    def getThreadId(self):
        u'''
        threadid のゲッター
        '''
        return self.thread_id

    def returnRes(self):
        u'''
        特定スレッドのレスの内容を表示する
        '''
        self.start = self.getStart()
        self.length = self.getLength()

        if self.start and self.length:
            return self.returnPirceRes()
        elif self.start:
            self.length = conf.RES_LENGTH # レスをデフォルトの値に指定する
            return self.returnPirceRes()
        else:
            return self.returnAllRes()

    def returnAllRes(self):
        u'''
        すべてのレスの内容を表示
        '''
        # スレッド名
        threadtitle = self.db.getThreadName(self.getThreadId())
        # レス
        reslist = self.db.threadIdToTakeRecord(self.getThreadId())
        # スレッド作成時アクセス先
        action = u'/makeres?no={0}'.format(self.getThreadId())
        return self.render.res(threadtitle, reslist, action)

    def returnPieceRes(self):
        u'''
        指定した範囲のレスを表示する
        '''
        reslist = self.db.threadIdAndLimitToTakeRecord(self.getThreadId(), 
                                                  self.start, self.length)
        action = u'/makeres?no={0}'.format(self.getThreadId())
        return self.render.res(reslist, action)
    
    
