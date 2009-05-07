#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import json
import os
import time

import web

class webclass(object):
    u'''
    web用処理クラス
    '''
    def __init__(self):
        try:
            fp = open(u'../conf.json', 'r')
            jsonobj = json.load(fp)
        finally:
            fp.close()
            
        self.filedir = jsonobj.get(u'filedir')
        self.realpath = jsonobj.get(u'realpath')
        self.tempdir = jsonobj.get(u'tempdir')
        self.title = jsonobj.get(u'title')
        self.dbpath = os.path.join(jsonobj.get(u'dbdir'),
                                   jsonobj.get(u'dbfile'))

    def GET(self):
        if self.__class__ == webclass:
            raise NotImplementedError
    def POST(self):
        if self.__class__ == webclass:
            raise NotImplementedError

class index(webclass):
    u'''
    index用クラス
    '''
    def __init__(self):
        super(index, self).__init__()

    def GET(self):
        self.db = sqlite3.connect(self.dbpath)
        rec = self.readFileRecord()
        self.db.close()
        render = web.template.Render(self.tempdir)
        return render.index(self.title, self.realpath,
                            self.filedir, self.makeUpForm(),
                            rec)
    def POST(self):
        web.seeother(u'/')

    def makeUpForm(self):
        uploadfile = web.form.File(u'uploadfile')
        comment = web.form.Textbox(u'comment')
        button = web.form.Button(u'send',
                                 type=u'submit')
        return web.form.Form(uploadfile,
                             comment,
                             button).render()
    def readFileRecord(self):
        query = u'''
                SELECT id, name, comment, uploadtime
                   FROM files
                   ORDER BY uploadtime DESC
                '''
        result = self.db.execute(query)
        return result.fetchall()


class upload(webclass):
    u'''
    アップロード用クラス
    '''
    def __init__(self):
        super(upload, self).__init__()
    def GET(self):
        web.seeother(u'/')
    def POST(self):
        self.post = web.webapi.input(uploadfile={})
        self.upfile = self.post.get(u'uploadfile')
        self.comment = self.post.get(u'comment')
        if self.checkUploadFile():
            try:
                self.db = sqlite3.connect(self.dbpath)
                self.fileUpload()
            except sqlite3.Error, e:
                for i in e.args:
                    print(i)
                self.db.rollback()
                self.db.close()
                sys.exit(0)
                
            self.db.commit()
            self.db.close()
            web.seeother(u'/')
            
        else:
            render = web.template.Render(self.tempdir)
            return render.error(u'エラーが発生しました。',
                                u'正しいファイルをアップロードしてください。',
                                u'/')
    def checkUploadFile(self):
        head = self.upfile.file.read(8)
        self.upfile.file.seek(0)
        chkExt = checkExtension(self.upfile.filename)
        chkHead = checkHeader(head)
        if (chkExt and chkHead and
            chkExt == chkHead):
            return True
        else:
            return False

    def makeFileName(self):
        import time
        import hashlib
        nowtime = str(int(time.time()))
        hs = hashlib.sha256(self.upfile.filename +
                            nowtime).hexdigest()[:5]
        ext = checkExtension(self.upfile.filename)
        return nowtime + hs + u'.' + ext

    def insertFileRecord(self):
        self.db.create_function(u'NOW', 0, NOW)
        query = u'''
                INSERT INTO files
                  (name, comment, uploadtime)
                  VALUES (:name, :comment, :uploadtime)
                '''
        now = time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime())
        param = {u'name' : self.savefilename,
                 u'comment' : self.comment,
                 u'uploadtime' : now}
        self.db.execute(query, param)
        return True

    def fileUpload(self):
        self.savefilename = self.makeFileName()
        count = self.getUploadFileCount()
        self.insertFileRecord()
        try:
            fp = open(os.path.join(
                      self.filedir,
                      self.savefilename),
                      u'wb')
            chunk = 1024 # 一度のロードサイズ
            while True:
                buf = self.upfile.file.read(chunk)
                if not buf:
                    break
                fp.write(buf)
        finally:
            fp.close()
            
        return True
            
    def getUploadFileCount(self):
        query = u'''
                SELECT count(id) `count`
                  FROM files
                '''
        result = self.db.execute(query)
        return result.fetchone()[0]

class chkloading(webclass):
    u'''
    ダウンロードさせるか、させないか
    '''
    def GET(self):
        self.post = web.webapi.input()
        self.render = web.template.Render(self.tempdir)
        if not self.post.get(u'file'):
            return self.render.error(u'不正なエラー',
                            u'正常な処理は行われませんでした<br/>' +
                            u'ファイルの情報がありません。',
                            u'/')
        
    def POST(self):
        web.seeother(u'/')

class loading(webclass):
    u'''
    アップロードされたファイルについてダウンロードさせる
    '''
    def GET(self):
        self.post = web.webapi.input()
        self.render = web.template.Render(self.tempdir)
        if not self.post.get(u'file'):
            return self.render.error(u'不正なエラー',
                        u'正常に処理は行われませんでした',
                        u'/')
        self.db = sqlite3.connect(self.dbpath)
        result = self.getUploadFileName()
        self.db.close()
        if not result:
            return self.render.error(u'ファイルえらー',
                        u'どうもファイルが正常にアップロードされてないみたいですよ',
                        u'/')

        fp = open(os.path.join(self.filedir,
                               result),
                  u'rb')
        print os.path.join(self.filedir,
                           result)
        dfp = fp.read()
        fp.close()
        web.header(u'Content-Disposition',
                   u'attachment; filename={0}'.format(result))
        web.header(u'Content-Type',
                   u'application/octet-stream')
        web.header(u'Content-Transfer-Encoding',
                   u'binary')
        web.header(u'Content-Length',
                   str(len(dfp)))
        return dfp
  
    def POST(self):
        web.seeother(u'/')

    def getUploadFileName(self):
        query = u'''
                SELECT name
                  FROM files
                  WHERE name = :name
                '''
        param = {u'name' : self.post.get(u'file')}
        result = self.db.execute(query, param)
        return result.fetchone()[0]
    
def checkExtension(filename):
    if (filename[-4:] == u'.jpg' or
        filename[-5:] == u'.jpeg'):
        return u'jpg'
    if (filename[-4:] == u'.gif'):
        return u'gif'
    if (filename[-4:] == u'.png'):
        return u'png'
    return False
    
def checkHeader(head):
    if head.startswith(b'\xff\xd8'):
        return u'jpg'
    if (head.startswith(b'gif87a') or
        head.startswith(b'gif89a')):
        return u'gif'
    if (head.startswith(b'\x89PNG\x0d\x0a\x1a\x0a')):
        return u'png'
    return False

def NOW():
    import time
    return time.strftime(u'%Y-%M-%D %h:%i:%s', time.localtime())
