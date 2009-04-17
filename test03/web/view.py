#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web
import os
import sys

if not u'../' in sys.path:
    sys.path.append(u'../')

from control import thread, index, res

urls = (
    u'/', u'index',
    u'/thread', u'thread',
    u'/res', u'res',
    u'/(.*)', u'index',
    )

def main():
    app = web.application(urls, globals())
    app.run()


if __name__ == u'__main__':
    main()
