from flask import Flask, render_template, request
import pymysql
from werkzeug.utils import redirect
#import BackEnd.crawler
#import time
import datetime
import json




app = Flask(__name__)

"""#数据库信息
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='Portfolio_Evaluation',
    charset='utf8'
)"""
app.debug = True


@app.route('/')
def index2():

    #content：url的字典
    return render_template("index.html",content = content)


"""@app.route('/delete/<path:i>')
def delete(i):
    print(type(i))
    sql = 'delete from fund where url = ' + i;
    cur2 = conn.cursor()
    cur2.execute(sql)
    conn.commit()
    return redirect("/")"""



#
@app.route('/spide', methods=["POST"])
def spide():
    #爬虫程序：
 a = request.form.get('url')
 print(a)
 return redirect('/')


if __name__ == "__main__":
       app.run()

