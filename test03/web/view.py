#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web
import os
import sys

if not u'../' in sys.path:
    sys.path.append(u'../')

from control import *

urls = (
    u'/', u'index',          # スレッド一覧表示
    u'/thread', u'mythread', # スレッド作成
    u'/res', u'res',         # レス作成、表示
    u'/error', u'error',     # エラー表示
    u'/(.*)', u'index',      # 条件に合わないものはスレッド一覧表示
    )

def main():
    app = web.application(urls, globals())
    app.run()


if __name__ == u'__main__':
    main()
