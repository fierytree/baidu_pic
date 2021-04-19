import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.90 Safari/537.36 '
}


def get_name(url2, tp):
    response = requests.get(url2, headers=headers)
    after_gzip = response.content
    response.encoding = 'utf-8'
    # t=after_gzip.decode("utf-8")
    # str2=t[t.find('div class="list_xz" id="listCont"'):t.find('span class="more" id="mxmore25"')]
    star_names = re.findall('href=\"/dy2013/mingxing/[0-9]{6}/[0-9]{1,5}.shtml\" title=\"([^\n\t]{1,30})\" class',
                            after_gzip.decode("utf-8"), re.S)
    star_num = re.findall('href=\"/dy2013/mingxing/([0-9]{6}/[0-9]{1,5}).shtml\" title=\"[^\n\t]{1,30}\" class',
                          after_gzip.decode("utf-8"), re.S)

    with open('manmankan_star_name.csv', 'a', encoding='utf-8') as f:
        for i in range(len(star_names)):
            f.write(star_names[i] + ',' + region[starType.index(tp)] + ',')
            f.write('http://www.manmankan.com/dy2013/mingxing/'+star_num[i]+'.shtml'+'\n')


starType = ['neidi', 'xianggang', 'taiwan', 'riben', 'hanguo', 'taiguo']
region = ['内地', '香港', '台湾', '日本', '韩国', '泰国']
for i in starType:
    url = 'http://www.manmankan.com/dy2013/mingxing/' + i + '/'
    print('开始爬取{}的明星'.format(region[starType.index(i)]))
    get_name(url, i)
