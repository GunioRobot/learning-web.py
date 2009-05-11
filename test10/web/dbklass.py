# -*- coding:utf-8 -*-

# builtin module
import time, sys, sqlite3

import web

class dbklass(object):
    u'''
    DBから情報ひっぱってくるメソッドとか集めた。
    '''
    def readFileRecord(self, start, length):
        u'''
        ファイル情報を求める
        '''
        query = u'''
                SELECT id, name, size, comment, uploadtime, delkey
                   FROM files
                   ORDER BY uploadtime DESC
                   LIMIT :start, :length
                '''
        param = {u'start' : start,
                 u'length' : length}
        result = self.db.execute(query, param)
        return result.fetchall()

    def getPageSize(self):
        u'''
        レコードの数を求める
        '''
        query = u'''
                SELECT COUNT(id)
                    FROM files
                '''
        result = self.db.execute(query)
        count = int(result.fetchone()[0])
        if count % self.pagesize != 0:
            rem = 1
        else:
            rem = 0
        return (count / self.pagesize + rem)

    def insertFileRecord(self):
        u'''
        ファイルの情報をテーブルに追加する
        '''
        query = u'''
                INSERT INTO files
                  (name, size, comment, uploadtime, delkey, addr)
                  VALUES (:name, :size, :comment, :uploadtime, :delkey, :addr)
                '''
        now = time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime())
        param = {u'name' : self.savefilename,
                 u'comment' : self.comment,
                 u'size' : self.filesize,
                 u'uploadtime' : now,
                 u'delkey' : self.delkey,
                 u'addr' : web.ctx.env['REMOTE_ADDR']}
        try:
            self.db.execute(query, param)
        except sqlite3.Error, e:
            for i in e.args:
                sys.stderr.write(i + '\n')
            self.db.rollback()
            return False

        return True

    def deleteFileRecord(self):
        u'''
        指定のファイルについて削除を行う
        削除できてなければFalseを返す
        削除できていればTrueを返す
        '''
        query = u'''
                DELETE FROM files
                  WHERE name = :filename
                '''
        param = {u'filename' : self.post.get(u'file')}
        result = self.db.execute(query, param)

        if not result.rowcount:
            return False
        else:
            return True
 
    def getUploadFileCount(self):
        u'''
        アップロードされたファイルの数の確認
        '''
        query = u'''
                SELECT count(id) `count`
                  FROM files
                '''
        result = self.db.execute(query)
        fetch = result.fetchone()
        if not fetch:
            return False
        else:
            return fetch[0]

    def getUploadFileName(self):
        u'''
        アップロードされたファイル名を確認する
        '''
        query = u'''
                SELECT name
                  FROM files
                  WHERE name = :name
                '''
        param = {u'name' : self.post.get(u'file')}
        result = self.db.execute(query, param)
        fetch = result.fetchone()
        if not fetch:
            return False
        else:
            return fetch[0]
