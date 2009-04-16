#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web

urls = (
    '/', 'index',
    )

class index(object):
    def GET(self):
        data = web.webapi.input()
        if data:
            keys = data.keys()
            s_keys = sorted(keys)
            for key in s_keys:
                yield 'key = ' + key + 'value = ' + data.get(key)
        else:
            yield 'hoge'

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
