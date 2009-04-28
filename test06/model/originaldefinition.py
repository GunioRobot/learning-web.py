# -*- coding:utf-8 -*-

# sqlite3では定義してないような関数を定義しとく
def NOW():
    u'''
    現在時刻を返す
    '''
    import time
    return time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime())
    
u'''
関数定義のリスト
[(使用する関数名, パラメータ数, 関数オブジェクト)]
'''
funclist = [
    (u'NOW', 0, NOW),
    ]