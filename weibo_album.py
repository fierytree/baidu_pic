import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import time
import random
import weibo_login

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.90 Safari/537.36 '
}
headers_login = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Content-Length': '166',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.weibo.cn',
    'Origin': 'https://passport.weibo.cn',
    'Referer': 'https://passport.weibo.cn/signin/login',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
                  'Version/11.0 Mobile/15A372 Safari/604.1 '
}

session = requests.Session()
data_login = {
    'username': '13971160579',
    'password': '2000420Dzj$',
    'savestate': '1',
    'r': '',
    'ec': '0',
    'pagerefer': '',
    'entry': 'mweibo',
    'wentry': '',
    'loginfrom': '',
    'client_id': '',
    'code': '',
    'qq': '',
    'mainpageflag': '1',
    'hff': '',
    'hfp': ''
}
url_login = 'https://passport.weibo.cn/sso/login'
path=r'E:\pic'
response_post = session.post(url=url_login, data=data_login, headers=headers_login)
print(response_post)


def save_pic(pic_data, save_path):
    cnt=0
    for temp in pic_data:
        for i in temp['pics']:
            pic_url=i['pic_big']
            file_lx=pic_url.split('.')[-1]
            if file_lx =='jpg' or file_lx=='png':
                response = requests.get(pic_url)
                print(pic_url)
                img = response.content
                with open(save_path + '\\%s.%s' % (str(time.time()), file_lx), 'wb') as f:
                    f.write(img)
                cnt+=1
    return cnt


def get(url):
    response = requests.get(url, headers=headers)
    after_gzip = response.content
    response.encoding = 'utf-8'
    return after_gzip.decode("utf-8")


def get2(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


def get_weibo_id(url):
    st = get(url)
    lst = re.findall('<a class=\"weibo\" href=\"http://weibo.com/([0-9]{1,20})\" target=\"_blank\"', st, re.S)
    return lst[0]


data = {}
with open('manmankan_star_name.csv', 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split(',')
        data[a[0]] = [a[1], a[2]]


# for item in data:
#     count=0
#     weibo_id = get_weibo_id(data[item][1])
#     data[item].append(weibo_id)
#     for k in range(100):
#         url1 = r'https://m.weibo.cn/api/container/getSecond?containerid=107803' + weibo_id +\
#                '_-_photoall&count=24&page=' + str(k) + '&title=图片墙&luicode=10000011&lfid=107803' + weibo_id + ''
#         response_text = session.get(url=url1)
#         js = json.loads(response_text.text)
#         data = js['data']['cards']
#         time.sleep(1)  # 控制抓取速度
#         count+=save_pic(data, path)
#     data[item].append(str(count))

count=0
weibo_id = get_weibo_id(data['赵丽颖'][1])
data['赵丽颖'].append(weibo_id)
for k in range(100):
    url1 = r'https://m.weibo.cn/api/container/getSecond?containerid=107803' + weibo_id +\
           '_-_photoall&count=24&page=' + str(k) + '&title=图片墙&luicode=10000011&lfid=107803' + weibo_id + ''
    response_text = session.get(url=url1)
    js = json.loads(response_text.text)
    data = js['data']['cards']
    time.sleep(1)  # 控制抓取速度
    count+=save_pic(data, path)
data['赵丽颖'].append(str(count))

f=open('weibo_pic.csv')
for item in data:
    for i in data[item]:
        f.write(i+',')
    f.write('\n')
