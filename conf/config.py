#!/usr/local/Cellar/python/3.7.1/bin
# -*- coding: UTF-8 -*-
import os
import urllib
from urllib import request
from bs4 import BeautifulSoup
import mysql.connector
import random
#*******************************通用变量定义***********************************************************
#设置数据库连接参数
mydb = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="lk",
        charset="utf8"
    )

# 设置headers
user_agents_list = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
]
user_agents = random.choice(user_agents_list)
headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    # 'Connection': 'Keep-Alive',
    'User-Agent': user_agents
}

#*******************************主函数入口***********************************************************
#获取网页重要信息并自动下载
def AutoGetHtmlMessage(url,i,imgname,proxies):
    # page = urllib.request.urlopen(url)
    # html = page.read().decode('UTF-8')
    html = getProxyHtml(url,proxies)
    soup = BeautifulSoup(html, "html.parser")
    # fwrite(soup.prettify())
    # print(soup.img['lazysrc'])
    # print(soup.prettify())
    # altstr = 'Rosimm.com - NO.2421[ROSI.CC - NO.2421]'
    imgurl = soup.img['lazysrc']
    # imgname = soup.img['alt']
    # imgurl = soup.id['allnum']
    #插入数据库
    # imgname = soup.img['alt']
    # getImgInsert(i,imgurl,imgname)
    #下载图片
    getImgDolad(imgurl,imgname,i)
    # message = {'imgurl':imgurl,'imgname':imgname,'imgnum':imgnum}
    return  True

#获取网页重要信息
def getHtmlMessage(html):
    soup = BeautifulSoup(html, "html.parser")
    # fwrite(soup.prettify())
    # print(soup.img['lazysrc'])
    # print(soup.prettify())
    # altstr = 'Rosimm.com - NO.2421[ROSI.CC - NO.2421]'
    imgurl = soup.img['lazysrc']
    imgname = soup.img['alt']
    # imgurl = soup.id['allnum']
    imgnum = soup.find('span', id='allnum').get_text()
    message = {'imgurl':imgurl,'imgname':imgname,'imgnum':imgnum}
    return  message

# 根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('UTF-8')

#*******************************数据库操作***********************************************************
# 查询数据库
def select_table():
    # 设置数据库连接参数
    mydb = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="lk",
        charset="utf8"
    )
    cursor = mydb.cursor(dictionary=True)  # 获取操作游标，也就是开始操作
    cursor.execute("select * from po_imgshowk")  # 执行查询语句
    data = cursor.fetchall()
    print(data)
    cursor.close()  # 关闭游标，结束操作
    mydb.close()  # 关闭数据库连接


# 清空数据
def trunc_table():
    # 设置数据库连接参数
    mydb = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="lk",
        charset="utf8"
    )
    cursor = mydb.cursor(dictionary=True)  # 获取操作游标，也就是开始操作
    sql = 'INSERT into po_imgshowk_his(IMAGENAME,IMAGEPATH) select IMAGENAME,IMAGEPATH from po_imgshowk'
    cursor.execute(sql)  # 执行查询语句
    sql = 'truncate table po_imgshowk'
    cursor.execute(sql)  # 执行查询语句
    mydb.commit()  # 数据表内容有更新
    cursor.close()  # 关闭游标，结束操作
    mydb.close()  # 关闭数据库连接

# 插入数据
def insert_table(imagename, imgurl):
    # 设置数据库连接参数
    mydb = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="lk",
        charset="utf8"
    )
    cursor = mydb.cursor(dictionary=True)  # 获取操作游标，也就是开始操作
    sql = 'insert into po_imgshowk(imagename,imagepath) VALUES(%s,%s)'
    val = (imagename, imgurl)
    cursor.execute(sql, val)  # 执行查询语句
    mydb.commit()  # 数据表内容有更新
    print(cursor.rowcount, "记录插入成功。")
    cursor.close()  # 关闭游标，结束操作
    mydb.close()  # 关闭数据库连接


# 图片处理--插入数据库
def getImgInsert(num, imgurl, imagename):
    # soup = BeautifulSoup(html,"html5lib")
    # soup = BeautifulSoup(html, "html.parser")
    # fwrite(soup.prettify())
    # print(soup.img['lazysrc'])
    # print(soup.prettify())
    # altstr = 'Rosimm.com - NO.2421[ROSI.CC - NO.2421]'
    # imgurl = soup.img['lazysrc']
    print("第" + format(num) + "张：" + imgurl)
    insert_table(imagename, imgurl)
    '''
    if num == 1:
        for imgurl in soup.find_all('img', alt=altstr):
            # print(imgurl.get('lazysrc'))
            str = imgurl.get('lazysrc')
            # insert_table(num,str)
    else:
        altstr1= altstr + '(' + format(num) + ')'
        for imgurl in soup.find_all('img',alt=altstr1):
            # print(imgurl.get('lazysrc'))
            str = imgurl.get('lazysrc')
            # insert_table(num,str)

    imgurl = soup.img['lazysrc']
    imgpath = 'Media/'+format(num)+'.jpg'
    urllib.request.urlretrieve(imgurl,imgpath)
    # return soup.img['lazysrc']


# 判断网页是否存在
def urlExits(url):
    try:
        response = urllib.request.urlopen(html, timeout=2)
        return 1
    except urllib.request.HTTPError as e:
        return 0
    except urllib.request.URLError as f:
        return 0
'''
#*******************************目录文件操作***********************************************************
# 图片处理 --下载本地
def getImgDolad(imageurl,imagename,num):
    # soup = BeautifulSoup(html,"html.parser")
    # fwrite(soup.prettify())
    # print(soup.img['lazysrc'])
    # imgurl = soup.img['lazysrc']
    imgpath = 'Media/' + imagename + '/' + format(num) + '.jpg'
    urllib.request.urlretrieve(imageurl,imgpath)
    print("第" + format(num) + "张("+imagename+")：" + imageurl)
    # return soup.img['lazysrc']

#创建目录函数
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

#写入文件函数
def fwrite(html):
    # 打开一个文件
    f = open("Media/pic.html", "w+")
    # 写入内容
    f.write(html)
    # 关闭打开的文件
    f.close()
#***************************************代理设置*********************************************
#代理函数，传url，返回html
def getProxyHtml(url,proxies):
    # proxies = {'http': '121.31.174.187:8123'}
    # proxies = select_valid_ip()
    # print(proxies)
    # 访问网址
    # url = "http://2018.ip138.com/ic.asp"
    # 创建ProxyHandler
    proxy_handler = request.ProxyHandler(proxies)
    # 创建Opener
    opener = request.build_opener(proxy_handler)
    # 安装headers
    opener.addheaders = [(k, v) for k, v in headers.items()]
    # 安装OPener
    request.install_opener(opener)
    # 使用自己安装好的Opener
    resp = opener.open(url, timeout=30)
    # 读取相应信息并解码
    # html = resp.read().decode('gbk')
    html = resp.read().decode('UTF-8')
    # 打印信息
    # print(html)
    return html

#测试ip有效性函数，传代理ip，返回status
def getProxyStatus(proxies):
    # 这是代理IP
    '''
    proxy_list = [
        {"http" : "124.88.67.81:80"},
        {"http" : "124.88.67.81:80"},
        {"http" : "124.88.67.81:80"},
        {"http" : "124.88.67.81:80"},
        {"http" : "124.88.67.81:80"}
    ]

    # 随机选择一个代理
    proxy = random.choice(proxy_list)
    '''
    # proxies = {'http': '121.31.174.187:8123'}
    # 访问网址
    # url = "http://2018.ip138.com/ic.asp"
    url = 'https://www.baidu.com'
    # 创建ProxyHandler
    proxy_handler = request.ProxyHandler(proxies)
    # 创建Opener
    opener = request.build_opener(proxy_handler)
    # 安装headers
    opener.addheaders = [(k, v) for k, v in headers.items()]
    # 安装OPener
    request.install_opener(opener)
    # 使用自己安装好的Opener
    # resp = opener.open(url, timeout=30)
    try:
        status = opener.open(url, timeout=2).code
    except:
        return 400
    else:
        return status
    # 读取相应信息并解码
    # html = resp.read().decode('gbk')
    # html = resp.read().decode('UTF-8')
    # 打印信息
    # print(html)
    return status

# 选出一个有效代理IP
def select_valid_ip():
    # 设置数据库连接参数
    mydb = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="root",  # 数据库密码
        database="lk",
        charset="utf8"
    )
    cursor = mydb.cursor(dictionary=True)  # 获取操作游标，也就是开始操作
    sql = 'select * from proxy_ip'
    cursor.execute(sql)  # 执行查询语句
    results = cursor.fetchall()
    # print(results)
    # print(cursor.rowcount, "记录插入成功。")
    while True:
        row = random.choice(results)
        ID = row['ID']
        type = row['type']
        address = row['address']
        port = row['port']
        proxies = {type + '\'': '\'' + address + ':' + port}
        status = getProxyStatus(proxies)
        if status == 400:
            continue
        else:
            break
    '''
    for row in results:
        ID = row['ID']
        type = row['type']
        address = row['address']
        port = row['port']
        # proxies = {row['ID'],row['type'],row['address'],row['port']}
        proxies = {type+'\'':'\''+address+':'+port}
        proxies_list.append(proxies)
        # th = threading.Thread(target=myproxy.getProxyStatus, args=(proxies,ID,address))
        # # ts.append(th)
        # th.start()
        # time.sleep(0.1)

        # status = myproxy.getProxyStatus(proxies)
        # if status == 400:
        #     print(ID,'失败')
        # else:
        #     print(ID,address,'有效')
    '''
    cursor.close()  # 关闭游标，结束操作
    mydb.close()  # 关闭数据库连接
    return proxies