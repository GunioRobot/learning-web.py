#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import web
import sqlite3

class thread(object):
    def GET(self):
        web.seeother(u'/')
    def POST(self):
        pass
