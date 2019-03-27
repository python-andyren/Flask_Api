import requests
import json

url = 'http://data.linlang.com/Data_api/get_buy_info_hl'

data = {
    'check_time': '1553595767',
    'sign': '794ba114aaf9dc99305a19be14d69d80',
}

content = requests.post(url=url, data=data).text

print(content)