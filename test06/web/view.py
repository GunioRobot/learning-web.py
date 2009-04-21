#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web

urls = (
    u'/', u'bbs',
    u'/thread', u'thread',
    u'/res', u'res',
    u'/rss', u'rss',
    )

def main():
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
