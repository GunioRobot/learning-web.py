#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# webアクセスで叩かれる場所

import web

import os
import sys
if not os.path.join(os.curdir, os.path.abspath(u'..')) in sys.path:
    sys.path.append(os.path.join(os.curdir, os.path.abspath(u'..')))

# 各モジュールインポート
from view.bbs import bbs
from view.bbsindex import bbsindex
from view.threadres import threadres
from view.makethread import makethread
from view.makeres import makeres

u'''
アクセス先パスと、
対応するクラス名
'''
urls = (
    u'/', u'bbsindex',            # BBS一覧
    u'/bbs', u'bbs',              # 特定BBS指定
    u'/thread', u'threadres',     # 特定スレ指定
    u'/res', u'res',              # レス関係
    #u'/rss', u'rss',
    u'/makethread', u'makethread',# スレッド作成
    u'/makeres', u'makeres',       # レス作成
    u'/.*', u'bbsindex',          # マッチしなかったものはBBS一覧へ
    )

def main():
    app = web.application(urls, globals())
    app.run()

if __name__ == u'__main__':
    main()
