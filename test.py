
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

data = {
    'url': 'https://img.alicdn.com/imgextra/i3/3603001646/O1CN01zFDRSS1O1uQEuEHWV_!!3603001646.jpg',
}


content = requests.post(url=url,data=data).json()

end = time.clock()

t=end-start

print("Runtime is ：",t)

print(content)




# 0.16