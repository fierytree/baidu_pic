import os
import signal
import json
import requests
import re
import matplotlib.pyplot as plt
import cv2
from retinaface_cov import RetinaFaceCoV
from io import BytesIO
import numpy as np


class InputTimeoutError(Exception):
    pass


def interrupted(signum,frame):
    raise InputTimeoutError


def decode_url(url):
    """
    对百度加密后的地址进行解码
    :param url:百度加密的url
    :return:解码后的url
    """
    if not url:
        return None
    table = {'w': "a", 'k': "b", 'v': "c", '1': "d", 'j': "e", 'u': "f", '2': "g", 'i': "h",
             't': "i", '3': "j", 'h': "k", 's': "l", '4': "m", 'g': "n", '5': "o", 'r': "p",
             'q': "q", '6': "r", 'f': "s", 'p': "t", '7': "u", 'e': "v", 'o': "w", '8': "1",
             'd': "2", 'n': "3", '9': "4", 'c': "5", 'm': "6", '0': "7",
             'b': "8", 'l': "9", 'a': "0", '_z2C$q': ":", "_z&e3B": ".", 'AzdH3F': "/"}
    url = re.sub(r'(?P<value>_z2C\$q|_z\&e3B|AzdH3F+)', lambda matched: table.get(matched.group('value')), url)
    return re.sub(r'(?P<value>[0-9a-w])', lambda matched: table.get(matched.group('value')), url)


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
        json_data = json.loads(bt, strict=False)
        json_data = json_data.get('data')
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


def get_image_url(url):
    image_url = []
    image_url2 = []
    response = requests.get(url, headers=headers)
    json_data = get_jason(response.text)
    if json_data is None:
        return [],[]
    for i in json_data:
        if i:
            image_url.append(decode_url(i.get('objURL')))
            image_url2.append(i.get('thumbURL'))
    if len(image_url) >= 1:
        del image_url[len(image_url) - 1]
    return image_url, image_url2


def save_pic(org_url, url, save_path,detector):
    response1 = requests.get(org_url, headers=headers_image)
    #print('原图链接:{}'.format(org_url))
    img = response1.content
    if len(img) < 500:
        #print('无原图，备用链接:{}'.format(url))
        response2 = requests.get(url, headers=headers_image)
        img = response2.content
    file_lx = 'jpg'
    if 'png' in url:
        file_lx = file_lx.replace('jpg', 'png')
    try:
        img_data = plt.imread(BytesIO(img),file_lx)
    except Exception as e:
        print(e)
        return
    faceDet(img_data,scales,detector,1,save_path + '/' + str(cnt) + '.' + file_lx)
    # cv2.imwrite(save_path + '\\' + str(cnt) + '.' + file_lx,img)
    # with open(save_path + '\\' + str(cnt) + '.' + file_lx, 'wb') as f2:
    #     f2.write(img)


def faceDet(img,scales,detector,count,filename):
    if img.size==0:
        return
    try:
        im_shape = img.shape
        target_size = scales[0]
        max_size = scales[1]
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        im_scale = float(target_size) / float(im_size_min)

        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)

        # print('im_scale', im_scale)

        n_scales = [im_scale]
        for c in range(count):
            faces,_ = detector.detect(img,thresh,scales=n_scales,do_flip=flip)

        if faces is not None:
            # print('find', faces.shape[0], 'faces')
            for i in range(faces.shape[0]):
                #print('score', faces[i][4])
                face = faces[i]
                box = face[0:4].astype(np.int)
                mask = face[5]
                x,y = box[2]-box[0],box[3]-box[1]
                img = img[box[1]:box[3],box[0]:box[2]]
                if img.size>0:
                    img = cv2.resize(img,(250,250))
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    cv2.imwrite(filename, img)
    except Exception as e:
        print(e)


thresh = 0.8
mask_thresh = 0.2
count = 1
flip = True
gpuid = 0
path = '/home/ubuntu/zzc/faceRecog/data'
data = {}
requests.DEFAULT_RETRIES = 5
n=0
last_name = 'Angelababy'
detector = RetinaFaceCoV('/home/ubuntu/zzc/faceRecog/faceRecog-main/model/mnet_cov2', 0, gpuid, 'net3l')

with open('/home/ubuntu/zzc/faceRecog/faceRecog-main/baidu_pic_count4.csv', 'r', encoding='utf-8') as f:
    for line in f:
        a = line.strip().split(',')
        data[a[0]] = [a[1], int(a[3]), n, cnt]

scales = [640, 1080]
cnt=0
# import multiprocessing
# pool = multiprocessing.Pool(processes=4)
for item in data:
    dirs=os.listdir(path + '/' + item)
    if len(dirs)!=0:
        continue
    cnt+=1
    # print(item+'start')
    # for i in range(data[item][1] // 30):
    #     url1 = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={' \
    #            '}&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={' \
    #            '}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&cg=star&pn={' \
    #            '}&rn=30&gsm=3c&1616411541408='.format(item, item, 30 * i)
    #     pic_org, pic_urls = get_image_url(url1)
    #
    #     arg = []
    #     for j in range(len(pic_org)):
    #         # arg.append(tuple([pic_org[j], pic_urls[j], path + '/' + item,detector]))
    #         signal.signal(signal.SIGALRM, interrupted)
    #         signal.alarm(10)
    #         try:
    #
    #             save_pic(pic_org[j], pic_urls[j], path + '/' + item, detector)
    #             cnt += 1
    #             print('已下载{}张图片'.format(cnt))
    #         except Exception as e:
    #             print(e)
    #         signal.alarm(0)
print(cnt)
