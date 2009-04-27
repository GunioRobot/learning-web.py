#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# webアクセスで叩かれる場所

import web

import os
import sys
if not os.path.join(os.curdir, os.path.abspath(u'..')) in sys.path:
    sys.path.append(os.path.join(os.curdir, os.path.abspath(u'..')))

from view.bbsindex import bbsindex
from view.bbs import bbs
from view.threadres import threadres

urls = (
    u'/', u'bbsindex',
    u'/bbs', u'bbs',
    u'/thread', u'threadres',
    u'/res', u'res',
    #u'/rss', u'rss',
    u'/.*', u'bbsindex',
    )

def main():
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
