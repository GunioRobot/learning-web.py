#!/usr/local/bin/python
# -*- coding:utf-8 -*-

# buildin module
import sqlite3, json, os, sys, time, hashlib, re

import Image
import web

from dbklass import dbklass

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
        self.maxupsize = jsonobj.get(u'maxupsize')
        self.pagesize = jsonobj.get(u'pagesize')
        self.commentlength = jsonobj.get(u'commentlength')

    def GET(self):
        if self.__class__ == webclass:
            raise NotImplementedError

    def POST(self):
        if self.__class__ == webclass:
            raise NotImplementedError

class index(webclass, dbklass):
    u'''
    index用クラス
    '''
    def GET(self):
        self.db = sqlite3.connect(self.dbpath)
        self.post = web.webapi.input()
        if (self.post.get(u'page') and
            re.match(r'^[0-9]+$', self.post.get(u'page'))):
            rec = self.readFileRecord((int(self.post.get(u'page'))-1) * self.pagesize,
                                      self.pagesize)
            if not rec:
                rec = self.readFileRecord(0, 10)
        else:
            rec = self.readFileRecord(0, 10)

        pagesize = self.getPageSize()
        self.db.close()

        render = web.template.Render(self.tempdir)
        web.header(u'Content-Type', u'text/html; charset=UTF-8')
        return render.index(self.title, self.realpath,
                            self.filedir, self.makeUpForm(),
                            rec, pagesize)
    def POST(self):
        web.seeother(u'/')

    def makeUpForm(self):
        uploadfile = web.form.File(u'uploadfile')
        comment = web.form.Textbox(u'comment')
        button = web.form.Button(u'send',
                                 type=u'submit')
        return web.form.Form(uploadfile, comment, button).render()



class upload(webclass, dbklass):
    u'''
    アップロード用クラス
    '''
    class uploadError(BaseException):
        u'''
        アップロード時のエラー
        '''
        pass

    def __init__(self):
        super(upload, self).__init__()

    def GET(self):
        web.seeother(u'/')

    def POST(self):
        self.post = web.webapi.input(uploadfile={})
        self.upfile = self.post.get(u'uploadfile')
        self.comment = self.post.get(u'comment')

        render = web.template.Render(self.tempdir)
        web.header(u'Content-Type', u'text/html; charset=UTF-8')
        if not self.checkComment():
            return render.error(u'不正なエラーが発生しました',
                                u'<b>コメントが長過ぎます</b><br/>' +
                                u'規定値 : {0}<br/>'.format(self.commentlength) +
                                u'受け取った文字数 : {0}'.format(len(self.comment)),
                                u'/')

        if self.checkUploadFile():
            try:
                self.db = sqlite3.connect(self.dbpath)
                self.fileUpload()
                self.insertFileRecord()
                self.db.commit()
                self.db.close()

            except self.uploadError, e:
                self.db.close()
                if e.msg == u'sizeover':
                    return render.error(u'エラーが発生しました',
                              u'アップしようとしてるファイルがでかすぎます。<br>' +
                              u'{0} KBまでのファイルだけが許されてます'.format(
                                                   self.maxupsize / 1024.0),
                              u'/')
          
            except sqlite3.Error, e:
                for i in e.args:
                    sys.stderr.write(i + '\n')
                self.db.rollback()
                self.db.close()
                sys.exit(0)
                
            web.seeother(u'/')
            
        else:
            return render.error(u'エラーが発生しました。',
                                u'正しいファイルをアップロードしてください。',
                                u'/')

    def checkComment(self):
        if len(self.comment) > self.commentlength:
            return False
        else:
            return True

    def checkUploadFile(self):
        u'''
        保存予定のファイルについて
        ヘッダのチェック, サイズチェックを行う
        '''
        filesizecount = 0
        while True:
            buf = self.upfile.file.read(1024)
            filesizecount += len(buf)
            # maxupsizeはバイトカウント :-)
            if (filesizecount <= self.maxupsize and
                not buf):
                self.upfile.file.seek(0)
                break
            elif filesizecount > self.maxupsize:
                self.upfile.file.seek(0)
                return False
        
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
        u'''
        ファイル名について適当に生成
        '''
        nowtime = str(int(time.time()))
        hs = hashlib.sha256(self.upfile.filename +
                            nowtime).hexdigest()[:5]
        ext = checkExtension(self.upfile.filename)
        return nowtime + hs + u'.' + ext

    def fileUpload(self):
        self.savefilename = self.makeFileName() # ファイル名作成

        try:
            fp = open(os.path.join(self.filedir, self.savefilename),
                      u'wb')
            chunk = 1024 # 一度のロードサイズ
            chunkcount = 0
            while True:
                buf = self.upfile.file.read(chunk)
                chunkcount += len(buf)
                if chunkcount > self.maxupsize:
                    raise self.uploadError, u"sizeover"
                if not buf:
                    break
                fp.write(buf)
        finally:
            fp.close()
        # サムネイル保存
        img =  createThumb(os.path.join(self.filedir, self.savefilename))
        img.save(u'static/thumb/th_' + self.savefilename.split(u'.')[0] + '.jpg', u'JPEG')
        
        # サイズを求める
        try:
            size = os.stat(os.path.join(self.filedir, self.savefilename))[6] / 1024.0
            num, dec = str(size).split(u'.')[0], str(size).split(u'.')[1][:2]
            self.filesize = float(num + u'.' + dec)
                             
        except os.error, e:
            for i in e.args:
                sys.stderr.write(i + '\n')
            os.unlink(os.path.join(self.filedir, self.savefilename))
            return False

        return True

class chkloading(webclass, dbklass):
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
        # ファイル名について確認
        self.db = sqlite3.connect(self.dbpath)
        result = self.getUploadFileName()
        self.db.close()
        if not result:
            return self.render.error(u'不正なエラー',
                            u'ファイル名についておかしな物が含まれていました',
                            u'/')
        # クッキー食わせ
        ck = downsession()
        ck.setSession()
        render = web.template.Render(self.tempdir)
        web.header(u'Content-Type', u'text/html; charset=UTF-8')
        return render.downloadchoice(result, downsession.expiretime, 
                                          u'/', downsession.sessionname)

    def POST(self):
        web.seeother(u'/')

class loading(webclass, dbklass):
    u'''
    アップロードされたファイルについてダウンロードさせる
    '''
    def GET(self):
        self.render = web.template.Render(self.tempdir)
        ck = downsession()
        if not ck.getSession():
            return self.render.error(u'不正なエラーです',
                         u'ダウンロードについて、有効時間内に実行していただくか、<br>' +
                         u'ダウンロード一回につき一回クリックした後に保存するようにしてください。',
                         u'/')

        self.post = web.webapi.input()

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

        dfp = fp.read()
        fp.close()

        # cookie破棄
        ck.clearCookie()
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


class downsession(object):
    u'''
    ダウンロード時のセションチェック
    '''
    # セション名(クッキー名称)
    sessionname = u'downsession'
    # クッキーの有効時間
    expiretime = 60
    def __init__(self):
        try:
            fp = open(u'../conf.json', u'r')
            jsonfile = json.load(fp)
        finally:
            fp.close()
        self.dbpath = os.path.join(
                          jsonfile.get(u'dbdir'),
                          jsonfile.get(u'dbfile'))
    def setSession(self):
        u'''
        セションをセット
        '''
        import random
        randval = hashlib.sha256(str(int(time.time())) + 
                                 str(random.randint(0,100))).hexdigest()
        web.setcookie(self.sessionname.encode(u'ascii'),
                      randval, 
                      self.expiretime)
        # DBに書込み
        try:
            db = sqlite3.connect(self.dbpath)
            query = u'''
                    INSERT INTO downsession
                      (session, expiretime, inserttime)
                      VALUES
                      (:session, :expiretime, :inserttime)
                    '''
            exp = time.strftime(u'%Y-%m-%d %H:%M:%S', 
                                time.localtime(time.time() + 
                                               self.expiretime))
            now = time.strftime(u'%Y-%m-%d %H:%M:%S',
                                time.localtime())
            param = {u'session' : randval,
                     u'expiretime' : exp,
                     u'inserttime' : now}
            db.execute(query, param)
        except sqlite3.Error, e:
            for i in e.args:
                print(i)
            db.rollback()
            db.close()
            return False
        
        db.commit()
        db.close()
        return True
    
    def getSession(self):
        u''' 
        セションをチェック
        ''' 
        try:
            cookie = web.cookies()
            if not cookie.get(self.sessionname):
                return False
         
            db = sqlite3.connect(self.dbpath)
            query = u'''
                    SELECT id
                      FROM downsession
                      WHERE session = :session
                    '''
            param = {u'session' : cookie.get(self.sessionname)}
            cur = db.execute(query, param)
            result = cur.fetchone()
            if not result:
                return False
            else:
                return True
 
        except AttributeError, e:
            u'''
            クッキーが存在しない場合
            '''
            return False

    def clearCookie(self):
        web.setcookie(self.sessionname.encode(u'ascii'), 
                      u''.encode(u'ascii'), 0)

def createThumb(image):
    u'''
    サムネイル作成
    '''
    img = Image.open(image)
    imgwidth, imgheight = img.size
    if imgwidth / 4 > 4:
        imgwidth /= 4
    if imgheight /4 > 4:
        imgheight /= 4
    return img.resize((imgwidth, imgheight))
    
def checkExtension(filename):
    u'''
    ファイル拡張子のチェック
    '''
    if (filename[-4:] == u'.jpg' or
        filename[-5:] == u'.jpeg'):
        return u'jpg'
    if (filename[-4:] == u'.gif'):
        return u'gif'
    if (filename[-4:] == u'.png'):
        return u'png'
    return False
    
def checkHeader(head):
    u'''
    ファイルヘッダのチェック
    '''
    if head.startswith(b'\xff\xd8'):
        return u'jpg'
    if (head.startswith(b'gif87a') or
        head.startswith(b'gif89a')):
        return u'gif'
    if (head.startswith(b'\x89PNG\x0d\x0a\x1a\x0a')):
        return u'png'
    return False

