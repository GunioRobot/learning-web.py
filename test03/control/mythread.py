#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web
import sqlite3

from model import *

class mythread(object):
    def GET(self):
        web.seeother(u'/')
    def POST(self):
        catch = web.input()
        post = checkPost_Thread(catch)
        # dbに書き込み
        db = dbControl()
        # スレッド
        res_thread = db.newCreateThread(post)
        # レス
        post['thread_id'] = res_thread
        res_res = db.newCreateRes(post)
        if not res_thread or not res_res:
            db.rollback()
            db.close()
            web.seeother(u'/error')
        else:
            db.commit()
            db.close()
            web.seeother(u'/res?no={0}'.format(res_thread))


def checkPost_Thread(post):
    u'''
    /threadに対し、ポストの値について確認する
    確認した値について、dictで返す
    '''
    checkThread = [u'threadtitle', u'username', u'message']
    if not isinstance(post, web.storage):
        return False
    for i in checkThread:
        if not post.get(i):
            return False
    return {u'threadtitle': post.get(u'threadtitle'),
            u'username': post.get(u'username'),
            u'message': post.get(u'message')}
    
    
