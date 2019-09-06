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

def get_shop_userid(item_id):
    url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data={%22itemNumId%22%3A%22'+ item_id + '%22}'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'cookie2=1acb4dc20d8272959207057bf863df78; t=edef350c191acdc23bfb6acd4246b38d; _tb_token_=e306ed76e01ee; thw=cn; enc=mF3vwSxyqWenHAyovcWRC3IvlFQs1fSBBPdNRE7TXhlgdpCvibUQJ2OBlsRpaNZE48svFgDczoDAy20SBrFbMA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; ctoken=acoDqgTLtAhLMfJIfejzrhllor; ockeqeudmj=lFJZGUc%3D; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BKg6YiKU%2BSjhUOBTNZoiWxzY%3D; _w_app_lg=23; UM_distinctid=16cf01bb920f9-01a47ccd605636-38617706-240000-16cf01bb921dec; cna=Sw3QFarKZA0CAd5H/M9WPX9u; v=0; lgc=vinter%5Cu4E36%5Cu6668%5Cu66E6; dnk=vinter%5Cu4E36%5Cu6668%5Cu66E6; tracknick=vinter%5Cu4E36%5Cu6668%5Cu66E6; _cc_=WqG3DMC9EA%3D%3D; tg=0; uc3=nk2=Fb73KaM5e9j1KDMB&id2=UoezTpA0pYae%2FA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dByuPYmlNOu72VCe4%3D; csg=918a5fcf; skt=10a41f55637671aa; existShop=MTU2NzU3NTQ5Mw%3D%3D; uc4=id4=0%40UO%2B14YCAtKak0CTZ5TcNnavFNWk%2F&nk4=0%40Fw%2Bl89LIObN4fYTreMR1eR3qq4j7%2B%2BE%3D; mt=ci=17_1; _m_h5_tk=2adb733dcfd697ac2ce23c69520a2f52_1567763141479; _m_h5_tk_enc=da0fc2305f4ac855702736494609d824; linezing_session=xzbHH42ky9YG25W02HBo3bHs_1567754066925Ct1u_50; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=URm48syIYB3rzvI4Dim4&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTaH0A1C82jtw%3D%3D&tag=8&lng=zh_CN; isg=BJeXvlNrhpwWuwIzyHIKbmyWJg0hdGs2_GEQ4unEs2bNGLda8az7jlU6fvij8EO2; l=cBaUeaCcqsFhPTxoBOCi5uI8as_OSIRAguPRwN0Mi_5pJ1TsADbOkryXUe96VjWdtG8B4QHSHov9-etXmPRgTBH8sxAR.',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }


    content = requests.get(url=url, headers=headers).content.decode('utf8')

    shop_user_id = re.findall('"userId":"(.*?)",', content)[0]

    return shop_user_id



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





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)