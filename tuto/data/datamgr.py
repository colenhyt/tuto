# -*- coding: utf-8 -*-

__author__ = 'colen'
import MySQLdb

SQL_INSERT_URL = "insert into siteurl (temp_id,url,status,crdate) values(%s,%s,%s,now())"
SQL_INSERT_STEMPLATE = "insert into stemplate (sitekey,itemskeys,pagingkeys,status,crdate) values(%s,%s,%s,%s,now())"

class DataMgr():
    def __init__(self):
        self.aa = 0

    def conn(self):
      conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="123a123@", db="box",charset="utf8")
      return conn;

    def update(self,sqlstr,params,isBatch=False):
      conn = self.conn();
      cursor = conn.cursor()
      if (isBatch):
        cursor.executemany(sqlstr,params)
      else:
        cursor.execute(sqlstr,params)
      conn.commit()
      cursor.close()
      conn.close()

    def gettable(self,sqlstr):
        conn = self.conn();
        cursor = conn.cursor()
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def geturls(self,sitekey):
        sql = "select a.*,b.sitekey from siteurl a,stemplate b where a.temp_id=b.id and a.status=0 and a.sitekey='"+sitekey+"'"
        return self.gettable(sql)

    def getsitetemplates(self,sitekey):
        sql = "select * from stemplate where status=0 and sitekey="+sitekey
        return self.gettable(sql)

    def getwords(self,wordtype=1):
        sql = "select * from words where status is null and wordtype="+str(wordtype)
        return self.gettable(sql)

    def updateSiteurl(self,id,status=1):
      params = [status,id]
      self.update("update siteurl set status=%s where id=%s",params)

    def inserturls(self,urls):
     self.update(SQL_INSERT_URL,urls,True)

    def inserturl(self,temp_id,url):
      params = [temp_id,url,0]
      self.update(SQL_INSERT_URL,params)

    def insertSiteTemplate(self,sitekey,itemskeys,pagingkeys):
      params = [sitekey,itemskeys,pagingkeys,1]
      self.update(SQL_INSERT_STEMPLATE,params)

aa = DataMgr()
siteurl = [[1,'DFA',1],[1,'f23ff',5],[1,'ww1w',4]]
aa.inserturls(siteurl)
# bb = aa.geturls()
# for k in bb:
#     print k[1]