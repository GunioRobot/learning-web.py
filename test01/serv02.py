#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web

urls = (
    u'/(.*)', u'index',
    )

app = web.application(urls, globals())

class index(object):
    def GET(self, name=None):
        if name is None:
            name = u'test'
        render = web.template.render(u'templates')
        xlist = [u'うふふ',u'毎日が日曜日',u'許すマジ',u'dwango']
        return render.test_01(name, xlist)

if __name__ == u'__main__':
    app.run()
