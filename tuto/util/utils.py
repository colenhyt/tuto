# -*- coding: utf-8 -*-
# __author__ = 'colen'


def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return backitems

def sort_by_valuelen(d):
    items=d.items()
    backitems=[[len(v[1]),v[0]] for v in items]
    backitems.sort(reverse=True)
    sortkeys = []
    for k in backitems:
        sortkeys.append([k[1],k[0]])
    return sortkeys


#两个tag相似度分析得分:
def tagSameScore(tag1,tag2):
    # tag count:
    es1 = tag1.xpath("*")
    if (len(es1)>20):return 0        #tag 数量过大，拦截
    es2 = tag2.xpath("*")
    if (len(es1)!=len(es2)):return 0      #数量不一致，拦截
    tagnames1 = ""
    tagkeys1 = ""
    for e in es1:
        tagnames1 += "_"+e.tag
        tagkeys1 += e.tag+ ":".join(e.keys());
    tagnames2 = ""
    tagkeys2 = ""
    for e in es2:
        tagnames2 += "_"+e.tag
        tagkeys2 += e.tag+":".join(e.keys())
    if (tagkeys1==tagkeys2):                        #子节点一致，子节点属性一致
        return 1
    elif (tagnames1==tagnames2) :              #子节点名一致
        return 0.8
    return 0

def _isImgUrl(url):
  if (url.find("http")>=0 and (url.find(".jpg")>0 or url.find(".gif")>0 or url.find(".png")>0)):
    return True
  return False

def _filterIgnore(url,ignorekeys=[]):
  if (url.find("javascript")>0):
    a = 100
  for ig in ignorekeys:
    if (url.find(ig)>=0):
      return True
  if (len(url)>500):
    print url
    return True

  return False