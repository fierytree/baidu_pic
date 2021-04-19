import requests

headers_login={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'keep-alive',
        'Content-Length':'166',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'passport.weibo.cn',
        'Origin':'https://passport.weibo.cn',
        'Referer':'https://passport.weibo.cn/signin/login',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

session =requests.Session()
data_login={
        'username':'你的用户名',
        'password':'你的密码',
        'savestate':'1',
        'r':'',
        'ec':'0',
        'pagerefer':'',
        'entry':'mweibo',
        'wentry':'',
        'loginfrom':'',
        'client_id':'',
        'code':'',
        'qq':'',
        'mainpageflag':'1',
        'hff':'',
        'hfp':''
        }
url_login='https://passport.weibo.cn/sso/login'

response_post=session.post(url=url_login,data=data_login,headers=headers_login)

print(response_post)