# coding: utf-8

# python 2.x         python 3.x
# cookielib          http.cookiejar
# urllib             urllib.parse
# urllib2            urllib.request
# httplib            http.client

import sys
import os
import base64
import time
import io
import gzip

import urllib.request
import urllib.parse
import urllib.error


import http.cookiejar
import socket
import http.client

from urllib.error import URLError, HTTPError

# xml解析类
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree


import imghdr
import re
import threading
from time import ctime
rlock = threading.RLock()

address_list_file_path      = '.\\addr_list.xml'
inbox_list_file_path        = '.\\inbox_list.xml'
address_list_f_file_path    = '.\\addr_list_formated.txt'
inbox_list_f_file_path      = '.\\inbox_list_formated.txt'


g_header = {
    'Host': 'twebmail.mail.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Connection': 'keep-alive'}


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    u"·": "&#183;",
    u"°": "&#176;",
    # regular expression
    ".": r"\.",
    "^": r"\^",
    "$": r"\$",
    "{": r"\{",
    "}": r"\}",
    "\\": r"\\",
    "|": r"\|",
    "(": r"\(",
    ")": r"\)",
    "+": r"\+",
    "*": r"\*",
    "?": r"\?",
}


def html_escape(text):
    """Produce entities within text."""
    tmp = "".join(html_escape_table.get(c, c) for c in text)
    return tmp.encode("utf-8")


cookiefile = './cookies.dat'  # cookie临时存放地


# 可以输入为空的i_postdata和i_heads
# i_postdata 为空，则按网页默认参数执行功能
# i_heads 为空，则按默认传输格式进行传输,如txt
# o_html is unicode
def post_req(i_url, i_postdata, i_heads):

    t_postdata = urllib.parse.urlencode(i_postdata).encode(encoding='UTF8')

    req = urllib.request.Request(
        url=i_url,
        data=t_postdata,
        headers=i_heads, )

    res = urllib.request.urlopen(req)
    #print('res=', res)

    if res.info().get('Content-Encoding') == 'gzip':
        # gzip format
        #print('------- gzip --------')
        bi = io.BytesIO(res.read())
        gf = gzip.GzipFile(fileobj=bi, mode="rb")
        #o_html = gf.read().decode("gbk")
        o_html = gf.read().decode()
    else:
        # text format
        #print('------- html --------')
        o_html = res.read().decode()

    # print(o_html)
    return o_html


class Email163:
    user = ''
    cookie = None
    cookiefile = './cookies.dat'  # cookie临时存放地
    sid = None
    mailBaseUrl = 'http://twebmail.mail.163.com'

    # 注意版本不同，登录URL也不同
    mail_loginUrl_prefix = 'https://ssl.mail.163.com/entry/coremail/fcg/ntesdoor2?funcid=loginone&df=mail163_letter&from_web&funcid=loginone&iframe=1&language=-1&passtype=1&product=mail163&net=n&styple=-1&race=58_47_56_gz&uid='

    # good:
    #mail_loginUrl_prefix  = 'https://ssl.mail.163.com/entry/coremail/fcg/ntesdoor2?funcid=loginone&language=-1&passtype=1&iframe=1&product=mail163&from=web&df=email163&race=-2_45_-2_hz&style=10&net=t&skinid=null&module=&uid='

    def __init__(self, keyword=None, *args):
        self.keyword = keyword
        self.cookie = http.cookiejar.CookieJar()
        cookiePro = urllib.request.HTTPCookieProcessor(self.cookie)
        urllib.request.install_opener(urllib.request.build_opener(cookiePro))

    def login(self, user, pwd):

        self.user = user
        # 登录
        postdata = {
            'username': user,
            'password': pwd,
            'type': 1
        }

        html = post_req(self.mail_loginUrl_prefix + user, postdata, g_header)
        # print(html)

        #file_obj = open('C:\\Users\\CnYaoJie\\Desktop\\login_log.txt', 'w')
        # file_obj.write(html)
        # file_obj.close

        patt = re.compile('sid=([^"]+)', re.I)
        patt = patt.search(str(html))
        #print('patt=', patt)

        uname = user.split('@')[0]
        
        self.user = user
        if patt:
            self.sid = patt.group(1).strip()
            #print ('sid=', self.sid)
            print ('%s Login Successful.....' % (uname))
        else:
            print ('%s Login failed....' % (uname))

        # cookie保存
        # self.cook#ie.save(self.cookiefile)
        #print('cookie set:',self.cookie)

    def getInBox(self):
        '''
        获取邮箱列表
        '''
        print('\nGet mail lists.....\n')
        sid = self.sid
        url = 'http://twebmail.mail.163.com/js6/s?sid=' + \
            sid + '&func=mbox:listMessages'

        postdata = {
            'Host': 'twebmail.mail.163.com',
            'func': 'mbox:listMessages',
            'sid': sid,
            'uid': self.user,
            # 加上var则只读取前50条邮件
            #'var':'<?xml version="1.0"?><object><int name="fid">1</int><string name="order">date</string><boolean name="desc">true</boolean><int name="limit">50</int><int name="start">0</int><boolean name="skipLockedFolders">false</boolean><string name="topFlag">top</string><boolean name="returnTag">true</boolean><boolean name="returnTotal">true</boolean></object>'
        }

        html = post_req(url, postdata, g_header)
        # print(html)

        file_obj = open(inbox_list_file_path, 'w', encoding='utf8')
        file_obj.write(str(html))
        file_obj.close

        # 解析XML，转换成json
        # 说明：由于这样请求后163给出的是xml格式的数据，
        # 为了返回的数据能方便使用最好是转为JSON
        mailList = []
        tree = etree.fromstring(html)
        obj = None
        for child in tree:
            if child.tag == 'array':
                obj = child
                break

        # 这里多参考一下，etree元素的方法属性等，包括attrib,text,tag,getchildren()等
        #obj = obj[0].getchildren().pop()
        for child in obj:
            #print(obj.tag, obj.attrib)
            for x in child:
                attr = x.attrib

                if not x.text:
                    v = ' '
                else:
                    v = x.text

                if attr['name'] == 'from':
                    value = {'from': v}
                    # print('from=',value)
                    mailList.append(value)
                if attr['name'] == 'subject':
                    value = {'subject': v}
                    mailList.append(value)
        return mailList

    # 获取通讯录
    def address_list(self):
        '''
        获取通讯录
        '''
        sid = self.sid
        username = self.user
        # 请求地址

        # url = 'http://twebmail.mail.163.com/contacts/call.do?uid=' + username + '@163.com&sid=' + sid + \
        #    '&from=webmail&cmd=newapi.getContacts&vcardver=3.0&ctype=all&attachinfos=yellowpage,frequentContacts&freContLim=20'

        url = 'http://twebmail.mail.163.com/js4/s?sid=' + sid + \
            '&func=global:sequential&showAd=false&userType=browser&uid=' + \
            username
        #print(url)

        postdata = {
            #'func': 'global:sequential',
            #'sid': sid,
            #'uid': username,
            #'cmd': 'newapi.getContacts',
            'func': 'global:sequential',
            'showAd': 'false',
            'sid': sid,
            'uid': username,
            'userType': 'browser',
            'var': '<!--?xml version="1.0"?--><object><array name="items"><object><string name="func">pab:searchContacts</string><object name="var"><array name="order"><object><string name="field">FN</string><boolean name="desc">false</boolean><boolean name="ignoreCase">true</boolean></object></array></object></object><object><string name="func">pab:getAllGroups</string></object></array></object>'
        }

        html = post_req(url, postdata, g_header)
        # print(html)

        file_obj = open(address_list_file_path, 'w', encoding='utf8')
        file_obj.write(str(html))
        file_obj.close

        # 解析XML，转换成json
        # 说明：由于这样请求后163给出的是xml格式的数据，
        # 为了返回的数据能方便使用最好是转为JSON
        json = []
        tree = etree.fromstring(html)
        obj = None
        for child in tree:
            if child.tag == 'array':
                obj = child
                break
        # 这里多参考一下，etree元素的方法属性等，包括attrib,text,tag,getchildren()等
        obj = obj[0].getchildren().pop()
        for child in obj:
            for x in child:
                attr = x.attrib
                if attr['name'] == 'EMAIL;PREF':
                    value = {'email': x.text}
                    json.append(value)
        return json


if __name__ == "__main__":
    print ("程序开始运行")

    # 初始化
    mail163 = Email163()

    # 登录
    mail163.login('user name', 'password')
    time.sleep(1)

    elist = mail163.getInBox()

    file_handle = open(inbox_list_f_file_path, 'a')
    for dic in elist:
        # print('dic=',dic)
        for key in dic:

            v = dic[key]
            v = v.encode('gbk', 'replace').decode('gbk')

            if key == 'from':
                print ('主题: ', v, end='')
                file_handle.write('主题: ' + v)
            else:
                print ('\t\t   来自:', v)
                file_handle.write('\t\t   来自:' + v)
                file_handle.write('\n')

    file_handle.close

    addr =mail163.address_list()

    file_handle = open(address_list_f_file_path, 'a')
    
    for x in addr:
        print(x['email'])
        file_handle.write(x['email']+'\n')

    file_handle.close        

    print ("程序运行结束")
