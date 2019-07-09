#coding=utf-8
from flask import Flask,Response,request
from flask_bootstrap import Bootstrap
import pymysql
import json
import re
import time
import requests
import hashlib
import redis


r_cookie = redis.Redis(host='172.21.0.39', port=6379, password='23323WudweSB6eHQ', db='1')


app = Flask(__name__)
bootstrap = Bootstrap(app)

local_time = time.strftime('%Y%m%d', time.localtime(time.time()))


def md5_passwd():
    add_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    salt = 'jingdongkuaidi'
    str= add_time + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    return res

@app.route('/api/jd_express_num', methods=['GET', 'POST'])
def parse_shopuserid():
    #如果请求方式位Post
    if request.method == "POST":
        #获取post请求参数密钥
        secret_key = request.form.get('secret_key')
        #本地本地生成密钥
        md5_key = md5_passwd()
        #比对密钥
        if secret_key == md5_key:
            jd_cookie = r_cookie.get('jd_cookie')
            orderId = request.form.get('orderId')
            pickDate = request.form.get('pickDate')

            url = 'https://details.jd.com/lazy/getOrderTrackInfoMultiPackage.action'

            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'content-length': '85',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': jd_cookie,
                'origin': 'https://details.jd.com',
                'referer': 'https://details.jd.com/normal/item.action?orderid=94859380202&PassKey=F16C63FE66ACE772E8FCF7BF9CFD2A0C',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            # orderId 为订单单号
            # pickDate 为下单当天凌晨时间

            data = {
                'orderId': orderId,
                'pickDate': pickDate,
            }

            try:

                content = requests.post(url=url, headers=headers, data=data).text

                return Response(json.dumps(content), mimetype='application/json')


            except:
                return Response(json.dumps({'msg': '该数据已脱敏'}), mimetype='application/json')
        else:

            return Response(json.dumps({'msg': '密钥不正确'}), mimetype='application/json')

    elif request.method == "GET":
        return Response(json.dumps({'msg': 'Request Method Is Wrong!'}), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)