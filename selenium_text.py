#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import requests
import pymysql
from sshtunnel import SSHTunnelForwarder
import random
from lxml import etree

add_cookie = 'UM_distinctid=16975c397bc6c2-0ab89e82e3d363-36617902-240000-16975c397bddff; JSESSIONID=6D35A99AF9E9A2B39FAC4C1A4E665F8B; CNZZDATA4962612=cnzz_eid%3D1091340430-1552458700-%26ntime%3D1559024150; CNZZDATA1276815554=1771521902-1553735125-%7C1559025544'


def to_mysql(data):
    with SSHTunnelForwarder(
            ('120.132.65.133', 22),  # B机器的配置
            ssh_password=r'*:A8QDe(98KIJx07l\bRm5k/#/3a',
            ssh_username='root',
            remote_bind_address=('10.9.72.185', 3306)) as server:  # A机器的配置

        db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                     port=server.local_bind_port,
                                     user='root',
                                     passwd='8jN5N8T5v4K5',
                                     db='data_third')

        cursor = db_connect.cursor()

        sql = 'insert into shuangying_huoyingfu(ww,buyreputation,bussreputation,sex,favrate,regdate,amoyage,buyweeklyaver,querytime,real_name,vip_level,vip_info,tucao,tuzi,mihuan,huli,eyu,yegou,laoshu,disposalsitus,blacklist,label,averagetimes,consumpower,userarea,sendrate,buyfrequency,userrefund,terminal,add_time) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d")' % (
            data['ww'], data['buyreputation'], data['bussreputation'], data['sex'], data['favrate'], data['regdate'],
            data['amoyage'], data['buyweeklyaver'], data['querytime'], data['real_name'], data['vip_level'],
            data['vip_info'], data['tucao'], data['tuzi'], data['mihuan'], data['huli'], data['eyu'], data['yegou'],
            data['laoshu'], data['disposalsitus'], data['blacklist'], data['label'], data['averagetimes'],
            data['consumpower'], data['userarea'], data['sendrate'], data['buyfrequency'], data['userrefund'],
            data['terminal'], data['add_time'])
        # 执行sql语句
        try:
            cursor.execute(sql)
            db_connect.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            db_connect.rollback()
        cursor.close()
    db_connect.close()

fp = open('ll.txt', 'a+')

huolifu_url = 'http://admin123.linlang.com/comm_plat_linlang/userAccountInfoAllOld'

# huoyingfu = 'http://plm.huoyingfu.com/comm_plat_shuangying/out_bind_info'

re = requests.get(url=huolifu_url).json()

li = [i for i in re if ' ' not in i]

option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--headless')
driver = webdriver.Chrome(executable_path='/root/selenium_project/chromedriver', chrome_options=option)
add_time = int(time.strftime('%Y%m%d', time.localtime(time.time())))

url = 'http://app.tk1788.com/app/superscan/op.jsp?m=login&username=18601793325&password=665defb7cfa842f52650555321061622&type=1&sign=1559005417423splic234f3c983713bd460e7c8c978ee4f436'

driver.get(url)

def get_tag(name):
    headers_tag = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '49',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': add_cookie,
        'Host': 'app.tk1788.com',
        'Origin': 'http://app.tk1788.com',
        'Referer': 'http://app.tk1788.com/app/superscan/searchAliim.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }
    tag_data = {
        'm': 'tagSearch',
        'aliim': name
    }

    content3 = requests.post('http://app.tk1788.com/app/superscan/opQueryGem.jsp', data=tag_data, headers=headers_tag).json()

    tree = etree.HTML(content3['msg'])

    tag = tree.xpath('//span/text()')[0]

    # print(tag)

    return tag

for i in li:
    b_id = i['id']
    name = i['account_name']

    try:
        inputID = driver.find_element_by_id("aliim")

        inputID.clear()

        inputID.send_keys(name)

        driver.implicitly_wait(2)

        driver.find_element_by_id("costTypeCkwbtn").click()

        time.sleep(3)

        # driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div[2]/a[1]").click()

        # alert = driver.switch_to.alert
        #
        # alert.accept()
        #
        # driver.implicitly_wait(2)

        #获取基础数据
        buyreputation = driver.find_element_by_xpath('//*[@id="buyerCre"]').text
        bussreputation = driver.find_element_by_xpath('//*[@id="sellerCredit"]').text
        sex = driver.find_element_by_xpath('//*[@id="sex"]').text
        favrate = driver.find_element_by_xpath('//*[@id="received_rate"]').text
        regdate = driver.find_element_by_xpath('//*[@id="created"]').text
        amoyage = driver.find_element_by_xpath('//*[@id="registDay"]').text
        buyweeklyaver = driver.find_element_by_xpath('//*[@id="buyerAvg"]').text
        querytime = driver.find_element_by_xpath('//*[@id="queryTimeBase"]').text
        real_name = driver.find_element_by_xpath('//*[@id="nameconform"]').text
        vip_level = driver.find_element_by_xpath('//*[@id="vip_level"]').text
        vip_info = driver.find_element_by_xpath('//*[@id="vip_info"]').text

        #获取打标情况
        tuzi = driver.find_element_by_xpath('//*[@id="tztd"]').text
        mihuan = driver.find_element_by_xpath('//*[@id="mgtd"]').text
        huli = driver.find_element_by_xpath('//*[@id="hltd"]').text
        eyu = driver.find_element_by_xpath('//*[@id="hltd"]').text
        jiangquanchuzhi = driver.find_element_by_xpath('//*[@id="downNum"]').text
        black = driver.find_element_by_xpath('//*[@id="yunBlack"]').text


        # time.sleep(15)
        # try:
        #     tag = driver.find_element_by_xpath('//*[@id="tagText"]').text
        # except:
        #     tag = '该旺旺没有标签'
        #获取标签
        tag = get_tag(name)

        data = {
            'ww': name,
            'b_id': b_id,
            'buyreputation': buyreputation,
            'bussreputation': bussreputation,
            'sex': sex,
            'favrate': favrate,
            'regdate': regdate,
            'amoyage': amoyage,
            'buyweeklyaver': buyweeklyaver,
            'querytime': querytime,
            'real_name': real_name,
            'vip_level': vip_level,
            'vip_info': vip_info,
            'tuzi': tuzi,
            'mihuan': mihuan,
            'huli': huli,
            'eyu': eyu,
            'disposalsitus': jiangquanchuzhi,
            'blacklist': black,

            'label': tag,

            'add_time': add_time,

        }

        print(data)

        fp.write(str(data) + '\n')

        # to_mysql(data)


    except:
        result = EC.alert_is_present()(driver)

        if result:
            result.accept()
            print('旺旺名不合法')

        elif result is False:
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/div/button[1]').click()
                print('繁体旺旺')
            except:
                print('账号不存在')

    loop_time = random.randint(3, 6)

    time.sleep(loop_time)

driver.quit()

fp.close()