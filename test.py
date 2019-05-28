
import time
start = time.clock()
import requests
import json
import hashlib

def md5_passwd():
    add_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    salt = 'fuck_python'
    str= add_time + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    return res

secret_key = md5_passwd()

url = 'http://anzizhaopin.cn/api/parse_shopuserid'

data = {
    'shopuserid': 2794704899,
    'secret_key': secret_key
}

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'anzizhaopin.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}

content = requests.post(url=url, data=data, headers=headers).json()

print(content)