import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import time
import random
import os

cnt = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.90 Safari/537.36 '
}
headers_image = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 '
                  'Safari/537.36',
    'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl'
               '=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1557124645631_R&pv=&ic=&nc=1&z'
               '=&hd=1&latest=0&copyright=0&se=1&showtab=0&fb=0&width=&height=&face=0'
               '&istype=2&ie=utf-8&sid=&word=%E8%83%A1%E6%AD%8C '
}


def get_jason(bt):
    try:
        json_data = bt.json()
        json_data = json_data.get('data')
        return json_data
    except Exception as e:
        print("异常信息e：{}".format(e))
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = bt.text[int(error_index[0])]
            data_str = bt.text.replace(error_str, "")
            # print("替换异常字符串{} 后的文本内容{}".format(error_str, data_str))
            return get_jason(bt)


def get_image_url(url):
    image_url = []
    response = requests.get(url, headers=headers)
    json_data = get_jason(response)
    if json_data is None:
        return []
    for i in json_data:
        if i:
            image_url.append(i.get('thumbURL'))
    return image_url


def save_pic(url, save_path):
    response1 = requests.get(url, headers=headers_image)
    print(url)
    img = response1.content
    file_lx = url.split('.')[-1]
    if file_lx == 'jpg' or file_lx == 'png':
        with open(save_path + '\\' + str(cnt) + '.' + file_lx, 'wb') as f2:
            f2.write(img)


path = 'E:\\pic'
data = {}
with open('manmankan_star_name.csv', 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split(',')
        data[a[0]] = [a[1], a[2]]

last_name = ''
for item in data:
    last_name = item
    if not os.path.exists(path + '\\' + item):
        os.mkdir(path + '\\' + item)
    for i in range(14):
        url1 = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={' \
               '}&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={' \
               '}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&cg=star&pn={' \
               '}&rn=30&gsm=3c&1616411541408='.format(item, item, 30 * i)
        pic_urls = get_image_url(url1)
        for pic_url in pic_urls:
            save_pic(pic_url, path + '\\' + item)
            cnt += 1
            print('已下载{}张图片'.format(cnt))
        time.sleep(1)

with open('log.txt', 'r', encoding='utf-8') as f:
    f.write(last_name+'\n')
    f.write(str(cnt))
