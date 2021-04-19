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


def get_name(url2):
    response = requests.get(url2, headers=headers)
    html = response.text
    # response.encoding = 'utf-8'
    star_names = re.findall('.*?\"name\":\"(.*?)\",', html, re.S)
    with open('baidu_star_name.csv', 'a', encoding='utf-8') as f:
        for name in star_names:
            print(name,end=' ')
            print(json.loads(f'"{name}"'))
            f.write(json.loads(f'"{name}"'))
            f.write('\n')


rankType = [11, 10, 1, 2, 3, 4, 9, 8]
page = [56, 56, 19, 15, 11, 12, 6, 6]
for i in range(len(rankType)):
    for j in range(page[i]):
        url = 'http://baike.baidu.com/api/starflower/starflowerstarlist?weekType=thisWeek&rankType=' \
              + str(rankType[i]) + '&page=' + str(j)
        print('开始爬取第{}个明星类别的第{}页'.format(i, j + 1))
        get_name(url)
