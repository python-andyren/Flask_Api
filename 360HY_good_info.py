import requests
from lxml import etree
import time
import redis
import re
import pymysql
import random
from urllib.parse import quote, unquote

add_time = time.strftime('%Y%m%d', time.localtime(time.time()))


platform = '360好药'

r = redis.Redis(host='127.0.0.1', port=6379, db='1')



def get_express_price(item_id, sku_id):
    url = 'http://origin.360haoyao.com/items/getFreightInfo.action?callback=jQuery18303127592928672074_1567853243909&itemId={}&goodsNum=1&provinceId=1&_=1567853244425'.format(sku_id)

    headers = {
        'Referer': 'http://www.360haoyao.com/item/{}.html'.format(item_id),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }

    content = requests.get(url=url, headers=headers).text

    express_price = re.findall('"goodsFreight":(.*?),', content)[0]

    return express_price


def get_info(item_id, key_word):
    item_url = 'http://www.360haoyao.com/item/{}.html'.format(item_id)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'provinceId=1; islogin_merge=0; Hm_lvt_d69a759ccf3a7184844852dabec00bfe=1566977274; Hm_lvt_21936694257e7e343d2dbbaee538e9ee=1566977274; UM_distinctid=16cd71fbbafdad-082618b1746371-38617706-240000-16cd71fbbb0f37; nTalk_CACHE_DATA={uid:gy_1000_ISME9754_guestA5BACEC5-494B-6A}; NTKF_T2D_CLIENTID=guestA5BACEC5-494B-6AD5-429F-D71FBBD921C4; tracker_u=direct; vid=U44481567851346036; uid=UD0C71567851346037; CNZZDATA1256399051=1497702192-1566975242-http%253A%252F%252Fwww.360haoyao.com%252F%7C1567849448; keyWordsHistory=%E6%AC%A7%E5%94%90%E9%9D%99%7C%E6%AC%A7%E5%94%90%E5%AE%81%7C%E8%BE%BE%E5%85%8B%E5%AE%81; tcpos=q--0--s_result_1_100704960--0--listwarp-1-d-100704960--0--0--0--0; history=100704960%2C%20%E6%AC%A7%E5%94%90%E5%AE%81%20%E5%88%A9%E6%A0%BC%E5%88%97%E6%B1%80%E7%89%87%207%E7%89%87%3B%20; Hm_lpvt_d69a759ccf3a7184844852dabec00bfe=1567851620; JSESSIONID=EF43FE5DC5E8D5891AB4B7BC92796DA0; Hm_lpvt_21936694257e7e343d2dbbaee538e9ee=1567852221; _citem_count=0',
        'Host': 'www.360haoyao.com',
        'Referer': 'http://www.360haoyao.com/search?q={}&from_type=enter'.format(quote(key_word)),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }

    content = requests.get(url=item_url, headers=headers).content.decode('gbk')
    # print(content)

    tree = etree.HTML(content)

    good_describe = tree.xpath('//div[@class="dtlInfoMid"]/h1/span/text()')[0]
    print(good_describe)

    good_detail_text = ' '.join(tree.xpath('//div[@class="w790"]/table/tbody/tr//text()')).replace('\t', '').replace('\n', '').replace('\r', '')
    print(good_detail_text)

    product_company = re.findall('<tr><th>企业名称：</th><td>(.*?)</td></tr>', content)[0]
    print(product_company)

    sales_promotion = ''

    sku_id = re.findall("var item_skuId='(.*?)';", content)[0]
    express_price = get_express_price(item_id, sku_id)
    print(express_price)

    product_size = re.findall('<li title="(.*?)">规格：(.*?)</li>', content)[0][0]
    print(product_size)

    good_price = ''



get_info('100704960', '欧唐宁')
