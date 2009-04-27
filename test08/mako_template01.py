#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web
from web.contrib.template import render_mako

urls = (
    u'/', u'index',
    )

class index(object):
    def GET(self):
        render = render_mako(
                   directories=['templates'],
                   input_encoding=u'utf-8',
                   output_encoding=u'utf-8',)
        mlist = [unicode(chr(x)) for x in range(65, 91)]
        return render.mako(title=u'テストタイトル',
                           olist=mlist)
    def POST(self):
        web.seeother(u'/')

def main():
    app = web.application(urls, globals(), autoreload=True)
    app.run()

if __name__ == u'__main__':
    main() 

    
