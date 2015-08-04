# -*- coding: utf-8 -*-

__author__ = 'colen'
import MySQLdb

class DataMgr():
    def __init__(self):
        self.aa = 0

    def gettable(self,sqlstr):
        conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="123a123@", db="box",charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        conn.close()
        print result
        return result

    def geturls(self):
        sql = "select a.*,b.sitekey from siteurl a,sitekeys b where a.key_id=b.id and a.status=0"
        return self.gettable(sql)

    def getsitekeys(self):
        sql = "select * from sitekeys where status=0"
        return self.gettable(sql)

    def getwords(self,wordtype=1):
        sql = "select * from words where status is null and wordtype="+str(wordtype)
        return self.gettable(sql)

aa = DataMgr()
bb = aa.getwords(8)
for k in bb:
    print k[1]