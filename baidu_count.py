import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import time
import random
import os

data = {}
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
with open('manmankan_star_name.csv', 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split(',')
        data[a[0]] = [a[1], a[2]]


def get_jason(bt):
    try:
        json_data = json.loads(bt, strict=False)
        json_data = json_data.get('listNum')
        return json_data
    except Exception as e:
        print("异常信息e：{}".format(e))
        error_index = re.findall(r"\(char ([0-9]{1,10})\)", str(e))
        if len(error_index) == 0:
            return None
        error_str = bt[int(error_index[0])]
        if error_str != '\\':
            return None
        bt = bt.replace(error_str, "")
        return get_jason(bt)


f2 = open('baidu_pic_count.csv', 'a', encoding='utf-8')
cnt = 0
for item in data:
    url1 = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={' \
           '}&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={' \
           '}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&cg=star&pn={' \
           '}&rn=30&gsm=3c&1616411541408='.format(item, item, 30)
    response1 = requests.get(url1, headers=headers_image)
    s = get_jason(response1.text)
    if s is None:
        continue
    c = int(s)
    data[item].append(c)
    f2.write(item + ',')
    for j in data[item]:
        f2.write(str(j) + ',')
    f2.write('\n')
    cnt += 1
    if cnt % 10 == 0:
        print(cnt)
