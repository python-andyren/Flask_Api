from flask import Flask,Response,request
from flask_bootstrap import Bootstrap
import pymysql
import json
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', deubug=True)