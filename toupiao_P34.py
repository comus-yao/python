#coding: utf-8
import sys
import os


import urllib,urllib.request,cookielib,socket 
import re  
import threading  
from time import ctime  
rlock = threading.RLock()

import Image, ImageEnhance, ImageFilter  
import urllib, urllib2, cookielib, httplib

import StringIO  
import wmi

def Min(x, y):  
    if x > y:  
        return y;  
    return x;

def CheckCode(image_name="./20.jpeg"):  
    #去处 干扰点  
    im = Image.open(image_name)  
    enhancer = ImageEnhance.Contrast(im)  
    im = enhancer.enhance(10)  
    im = im.convert('1')  
  
    #im.save("img_final.jpg") #测试查看  
  
    s = 0      #启始 切割点 x  
    t = 0      #启始 切割点 y  
  
    w = 8      #切割 宽 +y  
    h = 10      #切割 长 +x  
  
    im_new = []  
    for i in range(4): #验证码切割  
        im1 = im.crop((s + w * i + i * 2, t, s + w * (i + 1) + i * 2, h))  
        im_new.append(im1)  
        #im1.save("numer" + str(i) + ".jpg")  
  
  
    #测试查看  
    ret = ""  
    for x in range(4):  
        xsize, ysize = im_new[x].size  
        gd = []  
        for i in range(ysize):  
            tmp = []  
            for j in range(xsize):  
                if( im_new[x].getpixel((j, i)) == 255 ):  
                    tmp.append(1)  
                else:  
                    tmp.append(0)  
            gd.append(tmp)  
        maxn = -1;  
        pos = -1;  
        for noi in range(10):  
            img = Image.open(str(noi) + ".jpg")  
            x_size, y_size = img.size  
            gp = []  
            for i in range(y_size):  
                tmp = []  
                for j in range(x_size):  
                    if( img.getpixel((j, i)) == 255 ):  
                        tmp.append(1)  
                    else:  
                        tmp.append(0)  
                gp.append(tmp)  
            cout = 0  
            total = Min(x_size, xsize) * Min(y_size, ysize) * 1.0  
  
            for i in range(ysize):  
                for j in range(xsize):  
                    if gp[i][j] == gd[i][j]:  
                        cout += 1;  
            tempmax = cout / total  
            if tempmax > maxn:  
                maxn = tempmax;  
                pos = noi  
        if pos == 8 or pos == 3:  
            ret = "0"  
            break;  
        ret = ret + str(pos);  
    return ret  
  
  
def DownloadImage():  
    urimg = urllib2.urlopen("http://info.zjnu.edu.cn/zqtp/imgchk/validatecode.asp").read()  
    img = Image.open(StringIO.StringIO(urimg))  
    img.save(r".\20.jpeg")  


def ChangeIp(x):  
    os.system("WindowsApplication1\\" + str("%03d" % x) + ".bat")

def Submit(cc):  
    post_data = urllib.urlencode(  
        {"161": "161", "170": "170", "185": "185", "164": "164", "157": "157", "validatecode": cc, "post": "post",  
         "vote_type": "1", "Submit": "%C8%B7%B6%A8"});  
    #print post_data  
    path = "http://info.zjnu.edu.cn/zqtp/check.asp"  
  
    req = urllib2.Request(path, post_data)  
    conn = urllib2.urlopen(req)  
    txt = conn.read()  
    print (txt)
    
    
if __name__ == "__main__":  
    print "程序开始运行".decode("utf-8")  
    #os.system(r"WindowsApplication1\001.bat")  
    for x in range(2, 250):  
        print "开始修改IP...".decode("utf-8"), str("%03d" % x) + ".bat"  
        ChangeIp(x)  
        print "IP修改成功！".decode("utf-8")  
        cj = cookielib.CookieJar()  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
        opener.addheaders = [('User-agent', 'Opera/9.23')]  
        urllib2.install_opener(opener)  
        while True:  
            try:  
                DownloadImage()  
            except Exception, ex:  
                cc = 0  
                break;  
            cc = CheckCode()  
            print cc;  
            if int(cc) != 0:  
                break;  
        if cc == 0:  
            print "IP修改有误，不准备投票，直接跳过....".decode("utf-8")  
            continue  
        print "准备开始投票".decode("utf-8")  
        print "|-------------------------------------------------------|"  
        Submit(cc)  
        print "|-------------------------------------------------------|"  
    print "程序运行结束".decode("utf-8")  
