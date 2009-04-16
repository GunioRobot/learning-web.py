#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web
import sys
import re

import bbs

urls = (
    u'/', u'index',
    u'/insert', u'insert',
    u'/.*', u'redirect' )

class index(object):
    u'''
    /index アクセス時に利用する
    投稿内容を表示する
    '''
    def __init__(self):
        u'''
        コンストラクタ
        '''
        self.db = bbs.bbs()
        
    def GET(self):
        u'''
        GET時のアクセス
        '''
        data = web.input()
        row = self.db.countRows()
        if (data.get(u'page') and
            re.match(ur'^[0-9]+$', data.get(u'page')) and
            (int(data.get(u'page'))-1) <= (row / bbs.PAGE)):
            limitstart = (int(data.get(u'page'))-1) * bbs.PAGE
        else:
            limitstart = 0
        mlist = self.db.catchRecord(limitstart, bbs.PAGE)
        count = len(mlist)
        render = web.template.render(u'templates')
        insert = u'/insert?page={0}'.format(data.get(u'page')) \
                 if data.get(u'page') else u'/insert'
        return render.bbstop(u'テスト掲示板',
                             insert,
                             row,
                             u'テスト掲示板',
                             mlist,
                             bbs.PAGE)
    def POST(self):
        u'''
        POST時のアクセス
        '''
        web.seeother(u'/')
    
class redirect(object):
    u'''
    意図しないアクセス時のリダイレクト用
    '''
    def GET(self):
        u'''
        GET
        '''
        web.seeother(u'/')
    def POST(self):
        u'''
        POST
        '''
        web.seeother(u'/')

class insert(object):
    u'''
    /insert にアクセスしてきた場合の処理
    '''
    def __init__(self):
        u'''
        コンストラクタ
        '''
        self.db = bbs.bbs()
        
    def GET(self):
        u'''
        GET
        GETでのアクセス時は、/にリダイレクトする
        '''
        web.seeother(u'/')

    def POST(self):
        u'''
        POST
        '''
        data = web.input()
        name = data.username
        message = data.message
        self.db.insertRecord(name, message)
        if data.get(u'page'):
            web.seeother('/?page={0}'.format(data.get(u'page')))
        else:
            web.seeother('/')


if __name__ == u'__main__':
    app = web.application(urls, globals())
    app.run()
