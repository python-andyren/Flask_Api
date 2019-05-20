#coding=utf-8
from flask import Flask,Response,request
from flask_bootstrap import Bootstrap
import pymysql
import json
import re
import requests
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/api')
def index():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='dd..0202', db='new_shopinfo', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM test"
    cur.execute(sql)
    u = cur.fetchall()
    lis = list(u)
    result = []
    for i in lis:
        item = {
            'id': i[0],
            'name': i[1],
            'age': i[2],
            'country': i[3],
        }
        result.append(item)
    conn.close()
    return Response(json.dumps({'result': result}), mimetype='application/json')

@app.route('/api/testpost', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        user = request.form.get('user')
        password = request.form.get('password')
        if user != 'root':
            return Response(json.dumps({'msg': 'wrong!'}), mimetype='application/json')
        elif password != 'dd..0202':
            return Response(json.dumps({'msg': 'wrong!'}), mimetype='application/json')
        else:
            conn = pymysql.connect(host='127.0.0.1', user='root', password='dd..0202', db='new_shopinfo',
                                   charset='utf8')
            cur = conn.cursor()
            sql = "SELECT * FROM test"
            cur.execute(sql)
            u = cur.fetchall()
            lis = list(u)
            result = []
            for i in lis:
                item = {
                    'id': i[0],
                    'name': i[1],
                    'age': i[2],
                    'country': i[3],
                }
                result.append(item)
            conn.close()
            return Response(json.dumps({'result': result}), mimetype='application/json')

    if request.method == "GET":
        return Response(json.dumps({'msg': 'request method is wrong!'}), mimetype='application/json')

@app.route('/api/parse_aliimg', methods=['GET', 'POST'])
def parse_img():
    #如果请求方式位Post
    if request.method == "POST":
        img_url = request.form.get('img_url')
        cdn = re.search(r'!!(.*?).jpg', img_url)
        img_cdn = cdn.group(1)
        url = 'https://hdc1.alicdn.com/asyn.htm?userId={}'

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }

        try:
            content1 = requests.get(url=url.format(img_cdn), headers=headers).text.replace(r"\r\n", '').replace(" ",'').replace(" ", '').replace(r'\"', '').replace(r'/', '').replace('<span>', '')
            pattern = re.compile(r'"categoryName":"(.*?)"')
            result = pattern.findall(content1)[0]

            if result == '基础版' or result == '专业版':
                type = '淘宝'
                company = ''
                re_shop_name = re.compile(r'tbwmdd.1.044>(.*?)<')
                shop_name = re_shop_name.findall(content1)[0]
                re_ww = re.compile(r'柜：(.*?)<')
                ww = re_ww.findall(content1)[0]

            else:
                type = '天猫'
                re_company = re.compile(r'公司名：<label><divclass=right>(.*?)<div>')
                company = re_company.findall(content1)[0]
                re_tmall_shop = re.compile(r'.htm>(.*?)<')
                shop_name = re_tmall_shop.findall(content1)[-1]
                ww = ''

            content2 = {
                'shop_type': type,
                'shop_name': shop_name,
                'ww': ww,
                'company_name': company
            }

            return Response(json.dumps(content2), mimetype='application/json')
        except:
            return Response(json.dumps({'msg': '该数据已脱敏'}), mimetype='application/json')

    #如果请求方式为Get
    if request.method == "GET":
        return Response(json.dumps({'msg': 'Request Method Is Wrong!'}), mimetype='application/json')


@app.route('/api/parse_shopuserid', methods=['GET', 'POST'])
def parse_shopuserid():
    #如果请求方式位Post
    if request.method == "POST":
        shopuserid = request.form.get('shopuserid')
        # cdn = re.search(r'!!(.*?).jpg', img_url)
        # img_cdn = cdn.group(1)
        url = 'https://hdc1.alicdn.com/asyn.htm?userId={}'

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }

        try:
            content1 = requests.get(url=url.format(shopuserid), headers=headers).text.replace(r"\r\n", '').replace(" ",'').replace(" ", '').replace(r'\"', '').replace(r'/', '').replace('<span>', '')
            pattern = re.compile(r'"categoryName":"(.*?)"')
            result = pattern.findall(content1)[0]

            if result == '基础版' or result == '专业版':
                type = '淘宝'
                company = ''
                re_shop_name = re.compile(r'tbwmdd.1.044>(.*?)<')
                shop_name = re_shop_name.findall(content1)[0]
                re_ww = re.compile(r'柜：(.*?)<')
                ww = re_ww.findall(content1)[0]

            else:
                type = '天猫'
                re_company = re.compile(r'公司名：<label><divclass=right>(.*?)<div>')
                company = re_company.findall(content1)[0]
                re_tmall_shop = re.compile(r'.htm>(.*?)<')
                shop_name = re_tmall_shop.findall(content1)[-1]
                ww = ''

            content2 = {
                'shop_type': type,
                'shop_name': shop_name,
                'ww': ww,
                'company_name': company
            }

            return Response(json.dumps(content2), mimetype='application/json')
        except:
            return Response(json.dumps({'msg': '该数据已脱敏'}), mimetype='application/json')

    #如果请求方式为Get
    if request.method == "GET":
        return Response(json.dumps({'msg': 'Request Method Is Wrong!'}), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', deubug=True)