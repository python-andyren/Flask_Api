
import time
start = time.clock()
import requests
import json

url = 'http://data.linlang.com/General/parse_ali_img'

# url_pardse_headers = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     'Connection': 'keep-alive',
#     'Content-Length': '104',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Cookie': 'FANTONGTONG_TOKEN=4f9dTp3%2FQENaqltlLYsNVHX3o3EVIlDQdJKSKuEKzzRhzgZBPRQLeJ0moKbG2VOnh2d39wmzMSEpgk8t; session_data=qsr507ie1rod17vein64v2qf688t8nlc',
#     'Host': 'data.linlang.com',
#     'Origin': 'http://data.linlang.com',
#     'Referer': 'http://data.linlang.com/ShopInfo/parse_show',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }
add_time = time.strftime('%Y%m%d', time.localtime(time.time()))

def md5_passwd():
    #satl是盐值，默认是123456
    add_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    salt = 'fuck_python'
    str= add_time + salt
    import hashlib
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    print(res)
    return res

a = md5_passwd()
b = '4204717c0c03ef54d88f8dde2aeec85e'

if a == b:
    print('yes')

else:
    print('no')