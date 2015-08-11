# -*- coding: utf-8 -*-

__author__ = 'colen'
import MySQLdb
from tuto.util.basic import *
from tuto.util.utils import *


SQL_INSERT_URL = "insert into siteurl (temp_id,url,urltext,cat,relate_url1,status,crdate) values(%s,%s,%s,%s,%s,%s,now())"
SQL_UPDATE_URL = "update siteurl set urltext=%s,cat=%s where url=%s"
SQL_INSERT_STEMPLATE = "insert into stemplate (sitekey,itemskeys,pagingkeys,status,crdate) values(%s,%s,%s,%s,now())"
SQL_INSERT_ITEM = "insert into siteitem (url1,name,item_type,crdate) values(%s,%s,%s,now())"

class DataMgr(Singleton):
    objs_locker =  threading.Lock()

    def __init__(self):
      self.aa = 10
      self.urlsmap = {}
      self.initData()

    def initData(self):
      sql_allurl = "select id,url,temp_id,status from siteurl"
      tuples = self.gettable(sql_allurl)
      for t in tuples:
        url = list(t)
        self.urlsmap[url[1]] = url
      print "初始化urls map:",len(self.urlsmap)

    def conn(self):
      conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="123a123@", db="box",charset="utf8")
      return conn;

    def update(self,sqlstr,params,isBatch=False):
      conn = self.conn();
      lastrowid = 0
      cursor = conn.cursor()
      if (isBatch):
        cursor.executemany(sqlstr,params)
      else:
        cursor.execute(sqlstr,params)
        lastrowid = int(cursor.lastrowid)
      conn.commit()
      cursor.close()
      conn.close()
      return lastrowid

    def gettable(self,sqlstr,params=None):
        conn = self.conn();
        cursor = conn.cursor()
        cursor.execute(sqlstr,params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def geturls(self,sitekey="",status=1,urlkey=""):
        sql = "select a.id,a.temp_id,a.url,a.cat,b.sitekey from siteurl a left join stemplate b on a.temp_id=b.id where a.status=%s"
        params = [status]
        if (len(sitekey)>0):
          sql += " and b.sitekey=%s"
          params.append(sitekey)
        if (len(urlkey)>0):
          sql += " and a.url like %s"
          params.append("%"+urlkey+"%")
        return self.gettable(sql,params)

    def getsitetemplates(self,sitekey):
      sql = "select id,sitekey,itemskeys, pagingkeys from stemplate where status=1 and sitekey='"+sitekey+"'"
      tuple = self.gettable(sql)
      temp = None
      if (len(tuple)>0):
        temp = list(tuple[0])
      return temp

    def getwords(self,wordtype=1):
        sql = "select * from words where status is null and wordtype=%s"
        return self.gettable(sql,[wordtype])

    def updateurl(self,url,temp_id=0,status=1):
      # self.objs_locker.acquire()
      # try:
        if (self.urlsmap.has_key(url)):
          self.urlsmap[url][2] = status
          params = [status,url]
          self.update("update siteurl set status=%s where url=%s",params)
        else:
          self.inserturl(url,temp_id=temp_id,status=status)
      # finally:
      #   self.objs_locker.release()

    def inserturls(self,urls,temp_id=0,relate_url1="",status=0):
      self.objs_locker.acquire()
      try:
        newitems = []
        updateitems = []
        newurls = []
        for url in urls:
          key = str(url[0])
          print key,self.urlsmap[key]
          if (key.find('http://order.jd.com/center/list.action')>=0):
            a = 10
          item = self.urlsmap[key]
          if (item!=None):
            if (len(url[1])>0 and _isImgUrl(url[1])==False):
              item[2] = url[1]
              updateitems.append(item)
              self.urlsmap[url[0]] = item
              continue
          newurls.append(url)
          item = [temp_id,url[0]]
          if (len(url)>1):        #url text
            item.append(url[1])
          else:
            item.append("")
          if (len(url)>2):          #cat
            item.append(url[2])
          else:
            item.append(-1)

          item.extend([relate_url1,status])
          newitems.append(item)
          self.urlsmap[key] = item

        if (len(newitems)>0):
          self.update(SQL_INSERT_URL,newitems,True)
          print "新增urls",len(newitems)
        if (len(updateitems)>0):
          self.update(SQL_UPDATE_URL,updateitems,True)
        return newurls
      except (KeyError):
        print 'aaa'
      finally:
        self.objs_locker.release()
        return []

    def inserturl(self,url,urltext="",cat=-1,relate_url="",temp_id=0,status=0):
      # self.objs_locker.acquire()
      # try:
        if (self.urlsmap.has_key(url)):return

        self.urlsmap[url] = [url,temp_id,status]
        params = [temp_id,url,urltext,cat,relate_url,0]
        self.update(SQL_INSERT_URL,params)
      # finally:
      #   self.objs_locker.release()

    def insertSiteTemplate(self,*params):
      params = [params[0],str(params[1]),str(params[2]),1]
      return self.update(SQL_INSERT_STEMPLATE,params)

    def hasSiteurl(self,url):
      return True

    def insertitems(self,items,itemtype=0):
      newitems = []
      for item in items:
        newitems.append([item[0],item[1],itemtype])
      self.update(SQL_INSERT_ITEM,newitems,True)


    @classmethod
    def at(cls):
      print cls


aa = DataMgr()

# bb = aa.getsitetemplates("sogou.com")
# a = aa.geturls(urlkey='jd.com')
# print (len(a))
# for k in bb:
#     print k[1]