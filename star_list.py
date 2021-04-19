import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import time
import random
import os
import pypinyin
data={}
f1=open('baidu_pic_count4.csv', encoding='utf-8')
f3=open('namelist1.txt')
f4=open('namelist2.txt')
f5=open('baidu_pic_count6.csv','w', encoding='utf-8')
n1=[]
n2=[]
lst1=[]
for line in f1:
    a = line.strip().split(',')
    lst1.append(a[0])


def check(s):
    if s in n1 or s in n2:
        return False
    return True


for line in f3:
    n1.append(line.strip())
for line in f4:
    n2.append(line.strip())

with open('baidu_pic_count.csv', 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split(',')
        c=int(a[4])
        if c<=30:
            continue
        if c>=240 and a[0] not in lst1:
            continue
        lst=pypinyin.pinyin(a[0],style=pypinyin.NORMAL)
        py_str=''.join([''.join(lst[i]) for i in range(len(lst))])
        if check(py_str):
            f5.write(a[0]+','+a[1]+','+a[4]+'\n')
