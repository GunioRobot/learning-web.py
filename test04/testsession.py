#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import time
try:
    import web
except ImportError, e:
    print(u'please web.py install!')
    sys.exit(1)

urls = (
    u'/', u'index',
    u'/session', u'session',
    )

class myDiskStore(web.session.DiskStore):
    u'''
    なんでgetメソッドないの?死ぬの?
    ''' 
    def get(self, k):
        try:
            return self[k]
        except KeyError, e:
            return None

SESSIONDIR = u'/session'

class index(object):
    def __init__(self):
        self.session = myDiskStore(SESSIONDIR)
    def GET(self):
        render = web.template.Render(u'.')
        return render.template(u'/session', self.session.get(u'test'))
    def POST(self):
        web.seeother(u'/')

class session(object):
    def __init__(self):
        self.session = myDiskStore(SESSIONDIR)
    def GET(self):
        web.seeother(u'/')
    def POST(self):
        self.session['test'] = time.strftime(u'%Y-%M-%D %h:%m:%s', time.localtime())
        web.seeother(u'/')

if __name__ == u'__main__':
    app = web.application(urls, globals())
    app.run()

    



    
