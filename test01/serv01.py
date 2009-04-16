#!/usr/local/bin/python2.6
# -*- coding: utf-8 -*-

import web

urls = (
    '/', 'index',
    )

app = web.application(urls, globals())

class index(object):
    u'''
    index
    '''
    def GET(self):
        return 'Hello world!'

if __name__ == '__main__':
    app.run()
