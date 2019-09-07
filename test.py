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


r_cookie = redis.Redis(host='127.0.0.1', port=6379, db='1')


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


def shopid_get_userid(shopid):
    url = 'https://favorite.taobao.com/popup/add_collection.htm?id={}&itemid={}&itemtype=0&ownerid=7c4deab98fd1e2bf3db7e205ff3cf587&scjjc=2'.format(
        shopid, shopid)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'cookie2=1acb4dc20d8272959207057bf863df78; t=edef350c191acdc23bfb6acd4246b38d; _tb_token_=e306ed76e01ee; thw=cn; enc=mF3vwSxyqWenHAyovcWRC3IvlFQs1fSBBPdNRE7TXhlgdpCvibUQJ2OBlsRpaNZE48svFgDczoDAy20SBrFbMA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; ctoken=acoDqgTLtAhLMfJIfejzrhllor; UM_distinctid=16cf01bb920f9-01a47ccd605636-38617706-240000-16cf01bb921dec; cna=Sw3QFarKZA0CAd5H/M9WPX9u; v=0; lgc=vinter%5Cu4E36%5Cu6668%5Cu66E6; dnk=vinter%5Cu4E36%5Cu6668%5Cu66E6; tracknick=vinter%5Cu4E36%5Cu6668%5Cu66E6; tg=0; mt=ci=17_1; linezing_session=xzbHH42ky9YG25W02HBo3bHs_1567754066925Ct1u_50; _m_h5_tk=10a0228f0ea8cde792f8e5457dcf9bdb_1567831579777; _m_h5_tk_enc=17fcf04af613ad03705abb901fcf00e4; unb=1671216250; uc3=nk2=Fb73KaM5e9j1KDMB&id2=UoezTpA0pYae%2FA%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dByuPd0a7NznW4X3c%3D; csg=5f471205; cookie17=UoezTpA0pYae%2FA%3D%3D; skt=cba6bfe6fc0bf058; existShop=MTU2NzgyMTkxNw%3D%3D; uc4=nk4=0%40Fw%2Bl89LIObN4fYTreMR1eR3nMLYjXpw%3D&id4=0%40UO%2B14YCAtKak0CTZ5TcNkMhhiSpA; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=%E6%9B%A600; _nk_=vinter%5Cu4E36%5Cu6668%5Cu66E6; cookie1=ACrmID%2FLnLGRkDJCgA%2BtXaogt9EDXM0O%2FtHQiu9LXS4%3D; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTaH0%2BVgXlJmA%3D%3D&tag=8&lng=zh_CN; isg=BOvrvjc3MkF6U263XB4eoqDyegkVqP-KwMU8Zl1oxyqB_Ate5dCP0oleUnw3R1d6; l=cBaUeaCcqsFhP3ntBOCanurza77OSIRYYuPzaNbMi_5dK6T6GWQOkrqAQF96VjWdt28B4QHSHov9-etXZr7rczyvXCDc.',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }

    content = requests.get(url=url, headers=headers).content.decode('utf8')

    userid = re.findall('sellerId: (.*?),', content)[0]

    return userid


def get_tm_company(shop_user_id):
    url = 'https://hdc1.alicdn.com/asyn.htm?userId={}'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }

    try:
        content1 = requests.get(url=url.format(shop_user_id), headers=headers).text.replace(r"\r\n", '').replace(" ",
                                                                                                            '').replace(
            " ", '').replace(r'\"', '').replace(r'/', '').replace('<span>', '')
        # pattern = re.compile(r'"categoryName":"(.*?)"')

        re_company = re.compile(r'公司名：<label><divclass=right>(.*?)<div>')
        company = re_company.findall(content1)[0]

        content2 = {
            'company_name': company
        }
    except:
        content2 = {}

    return content2


# a = shopid_get_userid('578377242850')
# b = get_tm_company(a)
# print(b)
# exit()



@app.route('/api/get_tmall_company', methods=['GET', 'POST'])
def parse_shopuserid():
    # 如果请求方式位Post
    if request.method == "POST":
        # 获取post请求参数密钥
        secret_key = request.form.get('secret_key')
        print('密钥为：%s' % secret_key)
        # 本地本地生成密钥
        md5_key = 'test_api'
        # 比对密钥
        if secret_key == md5_key:

            try:
                shop_id = request.form.get('item_id')
                print('item_id：%s' % shop_id)

                shop_user_id = shopid_get_userid(shop_id)
                print('shop_user_id：%s' % shop_user_id)

                result = get_tm_company(shop_user_id)
                print(result)

                return Response(json.dumps(result), mimetype='application/json')

            except:
                return Response(json.dumps({'msg': '联系管理员'}), mimetype='application/json')
        else:

            return Response(json.dumps({'msg': '密钥不正确'}), mimetype='application/json')

    elif request.method == "GET":
        return Response(json.dumps({'msg': 'Request Method Is Wrong!'}), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)