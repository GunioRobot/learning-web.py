# -*- coding:utf-8 -*-

u'''
レスの新規作成
'''

import web
import re
import sys

from control.newres import newres
from config import conf

class makeres(object):
    u'''
    レスの新規作成時
    '''
    class makeResError(BaseException):
        u'''
        レス作成時のエラー
        '''
        pass
    
    def GET(self):
        web.seeother(u'/')
        
    def POST(self):
        # パラメータチェック
        try:
            self.getInput()
            db = newres()
            if not self.checkParameter():
                raise self.makeResError, u"レス作成時にエラーが発生しました"
        
            # 書き込み処理
            result = db.newRes(self.getThreadId(),
                               self.getUserName(),
                               self.getMessage())
            if not result:
                raise self.makeResError, u"レス作成時にエラーが発生しました"
            else:
                web.seeother(u'/thread?no={0}'.format(self.getThreadId()))
        except self.makeResError, e:
            return e.message

    def getInput(self):
        u'''
        取得データについてインプット
        '''
        self.mixed = web.webapi.input()
        
    def checkParameter(self):
        if (self.getThreadId() and 
            self.getUserName() and
            self.getMessage):
                return True
        else:
            return False
    def getThreadId(self):
        u'''
        対象となるスレッドID取得
        '''
        if (self.mixed.get(u'no') and
            re.match(ur'^[1-9][0-9]{0,2}$', self.mixed.get(u'no'))):
                return self.mixed.get(u'no')
        else:
            return False 
        
    def getUserName(self):
        u'''
        ユーザ名を取得
        '''
        if self.mixed.get(u'username'):
            return self.mixed.get(u'username')
        else:
            return False
    
    def getMessage(self):
        u'''
        メッセージを取得
        '''
        if self.mixed.get(u'message'):
            return self.mixed.get(u'message')
        else:
            return False
        
        