#coding=utf-8
from flask import Flask,Response,request
from flask_bootstrap import Bootstrap
import pymysql
import json
import re
import time
import requests
import hashlib
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)
bootstrap = Bootstrap(app)

local_time = time.strftime('%Y%m%d', time.localtime(time.time()))

def md5_passwd():
    add_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    salt = 'fuck_python'
    str= add_time + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    return res


def sql_cookie(account_name):
    # with SSHTunnelForwarder(
    #         ('152.136.122.35', 22),  # B机器的配置
    #         ssh_password='bhJYTpK0Y1iJUY1f',
    #         ssh_username='root',
    #         remote_bind_address=('172.21.0.43', 3306)) as server:  # A机器的配置

        db_connect = pymysql.connect(host='106.75.119.186',  # 此处必须是是127.0.0.1
                                     port=4040,
                                     user='root',
                                     passwd='0UY$Npuj8FdUHJky2',
                                     db='renqibox_server')

        cursor = db_connect.cursor()

        sql1 = "SELECT cookie FROM cookie_pool where account='%s';" % account_name
        # 执行sql语句
        try:
            cursor.execute(sql1)
            li = list(cursor.fetchall())
            cookie = li[0][0]
            db_connect.commit()

            return cookie
        except Exception as e:
            print(e)
            db_connect.rollback()
        cursor.close()
        db_connect.close()


def get_cookie(cookie, orderId, pickDate):
    url = 'https://details.jd.com/lazy/getOrderTrackInfoMultiPackage.action'

    headers = {
        # ':authority': 'details.jd.com',
        # ':method': 'POST',
        # ':path': '/lazy/getOrderTrackInfoMultiPackage.action',
        # ':scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-length': '85',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://details.jd.com',
        'referer': 'https://details.jd.com/normal/item.action?orderid=94859380202&PassKey=F16C63FE66ACE772E8FCF7BF9CFD2A0C',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'orderId': orderId,
        'pickDate': pickDate,
    }

    content = requests.post(url=url, headers=headers, data=data).json()

    print(content)

    try:

        if content['multiPackageTrackInfoList'][0]['carriageInfo']['carrier'] == '京东快递':
            data = {
                'express_id': orderId,
                'express_company': '京东快递'
            }
            return data

        else:

            express_id = content['multiPackageTrackInfoList'][0]['trackGroupInfo']['shipId']


            if express_id == None:
                express_company = ''

            else:
                express_company = content['multiPackageTrackInfoList'][0]['trackGroupInfo']['thirdName']

            data = {
                'express_id': express_id,
                'express_company': express_company
            }

            return data

    except:

        data = {
            'express_id': '',
            'express_company': ''
        }

        return data


@app.route('/api/getJDExpress', methods=['GET', 'POST'])
def get_express():
    #如果请求方式位Post
    if request.method == "POST":
        #获取post请求参数密钥
        secret_key = request.form.get('secret_key')
        #本地本地生成密钥
        md5_key = md5_passwd()
        #比对密钥
        if secret_key == md5_key:
            # orderId 为订单单号
            # pickDate 为下单当天凌晨时间
            try:
                account_name = request.form.get('account_name')
                print(account_name)
                cookie = sql_cookie(account_name)
                print(cookie)
                orderId = request.form.get('orderId')
                print(orderId)
                pickDate = request.form.get('pickDate')
                print(pickDate)
                data = get_cookie(cookie, orderId, pickDate)


                return Response(json.dumps({'msg': 'ok', 'expressID': data['express_id'], 'expressCompany': data['express_company']}), mimetype='application/json')

            except:
                return Response(json.dumps({'msg': 'Please Contact Technology'}), mimetype='application/json')

        else:
            return Response(json.dumps({'msg': 'Secret Key Is Not Match'}), mimetype='application/json')

        # 如果请求方式为Get
    if request.method == "GET":
        return Response(json.dumps({'msg': 'Request Method Is Wrong'}), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
