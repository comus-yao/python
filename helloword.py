#coding: utf-8

#python 2.x         python 3.x
#cookielib          http.cookiejar
#urllib2            urllib.request
#httplib            http.client

import sys
import os


import urllib, urllib.request,urllib.parse
import http.cookiejar,socket, http.client

from urllib.error import URLError,HTTPError

import imghdr
import re  
import threading  
from time import ctime  
rlock = threading.RLock()



#url = 'http://mail.163.com/'
url = 'http://reg.163.com/logins.jsp?type=1&product=mail163&url=http://entry.mail.163.com/coremail/fcg/ntesdoor2?lightweight%3D1%26verifycookie%3D1%26language%3D-1%26style%3D1' 

header = {'Host': 'mail.163.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip,deflate,sdch',
          'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
          'Connection': 'keep-alive'}    

  

cookiefile = './cookies.dat' #cookie临时存放地

class Email163:

  def __init__(self,keyword = None, *args):
    self.keyword = keyword
    self.cookie = http.cookiejar.CookieJar()
    cookiePro = urllib.request.HTTPCookieProcessor(self.cookie)
    urllib.request.install_opener(urllib.request.build_opener(cookiePro))
        
        
  def login(self,user,pwd):
    # 登录              
    postdata = urllib.request.urlencode({
                'username':user,
                'password':pwd,
                'type':1
            })
    #注意版本不同，登录URL也不同
    req = urllib.request.Request(
        url='https://ssl.mail.163.com/entry/coremail/fcg/ntesdoor2?funcid=loginone&language=-1&passtype=1&iframe=1&product=mail163&from=web&df=email163&race=-2_45_-2_hz&module=&uid='+user+'&style=10&net=t&skinid=null',
        data=postdata,
        headers=header, )
    res = str(urllib.request.urlopen(req).read())
    #print res
    patt = re.compile('sid=([^"]+)',re.I)
    patt = patt.search(res)
         
    uname = user.split('@')[0]
    self.user = user
    if patt:
      self.sid = patt.group(1).strip()
      #print self.sid
      print '%s Login Successful.....'%(uname)
    else:
      print '%s Login failed....'%(uname)            
                    
  #cookie设置
  
  self.cj = cookielib.LWPCookieJar()
  self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
  urllib2.install_opener(self.opener)
  self.tryLogin(username, password)
 
 
 
def hand_cookie():  
  cookie = http.cookiejar.CookieJar()  
  #cookie_handler = urllib2.HTTPCookieProcessor(cookie)  
  #after add error exception handler  
  
  cookie_handler = NoExceptionCookieProcesser(cookie) 
   
  opener = urllib.request.build_opener(cookie_handler, urllib2.HTTPHandler)  
  url_login = url 
  params = {"username":"comus_yao","password":"11"}  
  opener.open(url_login, urllib.urlencode(params))  
  
  
  for item in cookie:  
    print( item.name,item.value)
  #urllib2.install_opener(opener)  
  #content = urllib2.urlopen(url).read()  
  #print len(content)  
  #得到重定向 N 次以后最后页面URL
    
    
    
def use_proxy():  
  enable_proxy = False  
  proxy_handler = urllib.request.ProxyHandler({"http":"http://proxyurlXXXX.com:8080"})  
  null_proxy_handler = urllib.request.ProxyHandler({})  
  if enable_proxy:  
    opener = urllib.request.build_opener(proxy_handler, urllib2.HTTPHandler)  
  else:  
    opener = urllib.request.build_opener(null_proxy_handler, urllib2.HTTPHandler)  
  #此句设置urllib2的全局opener  
  urllib.request.install_opener(opener)  
  content = urllib.request.urlopen(url).read()  
  print ("proxy len:",len(content))
  
class NoExceptionCookieProcesser(urllib.request.HTTPCookieProcessor):  
  def http_error_403(self, req, fp, code, msg, hdrs):  
    return fp  
  def http_error_400(self, req, fp, code, msg, hdrs):  
    return fp  
  def http_error_500(self, req, fp, code, msg, hdrs):  
    return fp


if __name__ == "__main__":  
   print ("程序开始运行")
   print(url)

   try:  
      req = urllib.request.Request(url, headers = header) 
      response = urllib.request.urlopen(req)                     
   except HTTPError as e:  
      print('Error code:',e.code)   
   except URLError as e:  
      print('Reason',e.reason)

   doc = response.read()
   print(doc)

  
   print ("程序运行结束")


# try:  
#      #response=urllib.request.urlopen(full_url)
#      response=urllib.request.urlopen(url_req)
      
#   except HTTPError as e:  
#      print('Error code:',e.code)   
#   except URLError as e:  
#      print('Reason',e.reason)  


# ues=url_values.encode(encoding='UTF8')  
#   full_url=urllib.request.Request(url,url_values)     

#    proxy_support=urllib.request.ProxyHandler({'sock5':localhost:1080'})
#    opener = urllib.request.build_opener(proxy_support)
#    urllib.request.install_opener(opener)       
