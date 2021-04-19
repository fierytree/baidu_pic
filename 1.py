import urllib.request
import os

url='http://www.manmankan.com/dy2013/mingxing/neidi/'
response=urllib.request.urlopen(url,timeout=3)

s='1.png'
file_lx='jpg'
if 'png' in s:
    file_lx = file_lx.replace('jpg', 'png')
print(file_lx)

with open('baidu.html','w',encoding='utf-8') as fp:
    fp.write(response.read().decode('utf-8'))