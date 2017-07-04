#coding=utf-8

import re
import sys
import json
import time
import random
import requests
from bs4 import BeautifulSoup




headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Accept-Language': 'zh-CN',
           'Referer': 'http://blog.csdn.net/?ref=toolbar'}

useragent=[
'sogou spider(http://www.sogou.com/search/spider.htm)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)' ,
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
'Baiduspider (http://www.baidu.com/search/spider.htm)',
'Googlebot/2.1 (http://www.googlebot.com/bot.html)',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/ ) ',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 Wifiwx 3.1.2 (m2oapp 1.0.1) m2oSmartCity_Wifiwx m2oSmartCity_wifiwx'
]

data = {"username":"",
        "password":"",
        "lt":"",
        "execution":"",
        "_eventId":"submit"}

def creat_head():
    for i in useragent:
        headers['User-Agent'] = i
        for j in refer:
            headers['Referer'] = j
            # time.sleep(1)
            csdn_read(articles_list)

def get_articles():
    html = requests.get('http://blog.csdn.net/%s/article/list/1?viewmode=contents' % user,headers=headers)
    # print html.content
    soup = BeautifulSoup(html.content, "lxml")
    article_total =soup.find(id="papelist").contents
    print '文章', article_total[1].text
    total,pages=re.findall('[1-9]\d*', article_total[1].text)
    article_dict={}
    for i in range(1,int(pages)+1):
        html = requests.get('http://blog.csdn.net/%s/article/list/%s?viewmode=contents' % (user, i), headers=headers)
        print html.url
        soup = BeautifulSoup(html.content, "lxml")
        article_list =soup.find_all(class_="list_item list_view")
        for article in article_list:
            article_titles, article_manages = article.contents[1],article.contents[3]
            # 文章url
            article_url =  article_titles.contents[3].a['href']
            # for title in article_titles.contents[3].a.stripped_strings:
                #文章名称
                # print title
            # 阅读数
            read_num = re.search(r'[1-9]\d*',article_manages.contents[3].text).group()
            article_dict[article_url]=read_num
    return article_dict

def login_to_get_info():
    session = requests.session()
    html = session.get('https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn')
    soup = BeautifulSoup(html.content, "lxml")
    for input in soup.form.find_all("input"):
        if input.get("name") == "lt":
            data['lt'] = input.get("value")
        if input.get("name") == "execution":
            data['execution'] = input.get("value")
    data['username'],data['password']=account, password
    html = session.post('http://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn', data=data,headers=headers)
    print html.content
    if "登录" in html.content:
        print "登录失败，请检查账号密码"
        return 1
    else:
        print  "登录成功"
        info = json.loads(re.search(r'data = ({.*})',html.content).group(1))
        for key in info.keys():
            print key, "：", info[key]

        return info['userName']



def start_read():
    for key,value in article_dict.items():
        if int(value) < random.randint(5000, 10000):
            random_num = random.randint(50, 99)
            for i in range(random_num):
                headers['User-Agent'] = random.sample(useragent,1)[0]
                html = requests.get('http://blog.csdn.net%s'%key,headers=headers)
            soup = BeautifulSoup(html.content, "lxml")
            print soup.title.string, "增加随机阅读次数", random_num



if __name__ == '__main__':

    user=''
    if user:
        time_start = time.time()
    else:
        account = raw_input('请输入登录邮箱或手机号：')
        password = raw_input('请输入密码：')
        time_start = time.time()
        user = login_to_get_info()
        if user == 1:
            print "运行失败"
        else:
            user
    article_dict = get_articles()
    start_read()
    time_end = time.time()
    print "此次运行耗时 %s 秒"%(time_end - time_start)