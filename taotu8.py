#!/usr/local/Cellar/python/3.7.1/bin
# -*- coding: UTF-8 -*-
# https://www.192tt.com （美图图片网站）
import sys
sys.path.append("conf/")
import config as myconf
import threading
import time
import urllib
from urllib import request
from bs4 import BeautifulSoup

url = 'https://www.192tt.com/gc/vgirl/vgirl011.html'
# print(fixedurl[:-5])
fixedurl = url[:-5]
html = myconf.getHtml(url)
MainMessage = myconf.getHtmlMessage(html)
# print('Media/' + MainMessage['imgname'])
myconf.mkdir('Media/' + MainMessage['imgname'])
# print(message['imgurl'])
# soup = BeautifulSoup(html,"html5lib")
# soup = BeautifulSoup(html, "html.parser")
# fwrite(soup.prettify())
# print(soup.img['lazysrc'])
# print(soup.prettify())
# altstr = 'Rosimm.com - NO.2421[ROSI.CC - NO.2421]'
# imgurl = soup.img['lazysrc']
# imgname = soup.img['alt']
# imgurl = soup.id['allnum']
# imgnum = soup.find('span', id='allnum').get_text()
# print(imgnum,imgname,imgurl)
# 主程序
# fixedurl = 'https://www.192tt.com/gc/rosimm/rosi2421'
myconf.trunc_table()
message = ''
ts = []
proxies = myconf.select_valid_ip()
print(proxies)
for i in range(1, int(MainMessage['imgnum'])+1):
    if i == 1:
        # html = myconf.getHtml(url)
        # message = myconf.AutoGetHtmlMessage(url,i,MainMessage['imgname'])
        th = threading.Thread(target=myconf.AutoGetHtmlMessage, args=(url,i,MainMessage['imgname'],proxies))
        # ts.append(th)
        th.start()
        time.sleep(0.1)
    else:
        url = fixedurl + "_" + format(i) + ".html"
        # html = myconf.getHtml(url)
        # message = myconf.AutoGetHtmlMessage(html,i,MainMessage['imgname'])
        th = threading.Thread(target=myconf.AutoGetHtmlMessage, args=(url,i,MainMessage['imgname'],proxies))
        # ts.append(th)
        th.start()
        time.sleep(0.1)
        # status = urllib.request.urlopen(url, timeout=1).code
        # if(status == 200):
        #     # print(fixedurl +getHtml(url) "_"+format(i)+".html")
        #     html = getHtml(url)
        # else:
        #     break
        # print("开始第" + format(i) + "线程！")

        # myconf.getImgInsert(i,message['imgurl'],MainMessage['imgname'])
    # myconf.getImgDolad(message['imgurl'],MainMessage['imgname'],i)

'''
#加锁和释放锁
mlock = threading.RLock()    #定义锁
mlock.acquire()    #加锁
#需要独占线程资源执行的代码
mlock.release()     #释放锁
'''