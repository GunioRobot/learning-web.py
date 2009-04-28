# -*- coding:utf-8 -*-

u'''
スレッドの新規作成
'''
import web
import re

from control.newthread import newthread
from config import conf

class makethread(object):
    u'''
    スレッドの作成を行う
    '''
    class MakeThreadError(BaseException):
        u'''
        スレッド作成に伴うエラー
        '''
        pass
    
    
    def GET(self):
        u'''
        GETの場合は無視
        '''
        web.seeother(u'/')
        
    def POST(self):
        self.getInput()
        if self.checkParameter():
            self.createThread()
            return u'スレッド作成しました。'
            import time
            time.sleep(2)
            web.seeother(u'/')
        else:
            web.seeother(u'/')
            return
    
    def getInput(self):
        u'''
        web.webapi.input より
        GET or POSTの値を得る
        '''
        self.mixed = web.webapi.input()
    
    def getMixed(self):
        u'''
        mixedのゲッター
        '''
        return self.mixed
            
    def createThread(self):
        u'''
        スレッド作成
        '''
        if not self.checkParameter():
            raise self.MakeThreadError, u"スレッド作成時にエラーでました。"
        
        db = newthread()
        result = db.newThread(self.getBbsId(), self.getThreadName(),
                              self.getUserName(), self.getMessage())
        if not result:
            raise self.MakeThreadError, u"スレッド作成時にエラーでました。"

        return True
        
        
    def checkParameter(self):
        u'''
        スレッド作成に必要なパラメータについてチェックする
        '''
        if (self.getThreadName() and
            self.getUserName() and
            self.getMessage()):
               return True
        else:
            return False
            
    def getBbsId(self):
        u'''
        bbsidを取得
        '''
        if self.mixed.get(u'no'):
            return self.mixed.get(u'no')
        else:
            return False
        
    def getThreadName(self):
        u'''
        スレッド名を取得
        '''
        if self.mixed.get(u'threadname'):
            return self.mixed.get(u'threadname')
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
        




