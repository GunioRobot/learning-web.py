#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web

urls = (
    u'/', u'index',
    )

class index(object):
    def GET(self):
        web.ctx.status = u'404 NotFound'
        return u'oh...'

    def POST(self):
        web.seeother(u'/')


def main():
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
