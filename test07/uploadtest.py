#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import web
import os
import sys
TEMP_INDEX = \
u'''
<html>
  <head>
  </head>
  <body>
    <div align="center">
      <h1>あっぷろーど</h1>
    </div>
    <div align="center">
      <form method="POST" action="/" enctype="multipart/form-data">
        <input type="file" name="upfile"><br/>
        <input type="submit" name="submit" value="upload">
      </form>
    </div>
  </body>
</html>
'''

urls = ('/', 'upload')

MAXSIZE = 1024 * 1024
class upload(object):
    def GET(self):
        index = web.template.Template(TEMP_INDEX)
        return index()
    def POST(self):
        u'''
        multipart/formdata , type="file"にて
        ファイルを受け取る場合、web.webapi.input()メソッドに
        キーワード引数と、デフォルト値には空dictを渡してあげる
        必要がある
        '''
        if not os.path.exists(u'upload'):
            os.mkdir(u'upload')
        mixed = web.webapi.input(upfile={})
        upfile = mixed[u'upfile']
        fp, fname = upfile.file, upfile.filename
        if not fp or not fname:
            web.seeother(u'/')
            return 
        savefile = open(os.path.join(u'upload', fname), 'wb')
        try:
            chunk = 2048
            readsize = 0
            while True:
                x = fp.read(chunk)
                readsize += chunk
                if readsize > MAXSIZE:
                    return u'ファイルでかすぎふざけんな max size: {0}'.format(MAXSIZE)
                if not x:
                    break
                savefile.write(x)
        finally:
            savefile.flush()
            savefile.close()

        web.seeother(u'/')

        
        
        
if __name__ == u'__main__':
    app = web.application(urls, globals())
    app.run()
 
