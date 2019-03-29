import requests
import json

url = 'http://127.0.0.1:5000/api/parse_aliimg'

data = {
    'img_url': 'https://img.alicdn.com/imgextra/i3/3603001646/O1CN01zFDRSS1O1uQEuEHWV_!!3603001646.jpg',
}


content = requests.post(url=url, data=data).json()

print(content)