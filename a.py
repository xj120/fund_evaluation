from flask import Flask, render_template, request
import pymysql
from werkzeug.utils import redirect
#import BackEnd.crawler
#import time
import datetime
import json




app = Flask(__name__)

#数据库信息
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='Portfolio_Evaluation',
    charset='utf8'
)
app.debug = True


@app.route('/')
def index2():
    cur = conn.cursor()
    sql = "select url from fund"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template("index.html", content = content)


@app.route('/delete/<path:i>')
def delete(i):
    print(type(i))
    sql = 'delete from fund where url = ' + i;
    cur2 = conn.cursor()
    cur2.execute(sql)
    conn.commit()
    return redirect("/")



#爬取一个URL，i[1]是URL
"""@app.route('/spide/<i>')
def spurl(i):
 BackEnd.crawler.geturlInfo(i[1])
 cur4 = conn.cursor()
 sql="update url  set found_date=" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) +"where url=" + i[1];
 cur4.execute(sql)
 conn.commit();
 return redirect("/")

#爬取全部URL，content是全部记录，i是单条记录，i[1]是URL
@app.route('/spideall/<content>')
def spideall(content):
    for i in content:
        BackEnd.crawler.geturlInfo(i[1])
        cur4 = conn.cursor()
        sql = "update url  set found_date=" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "where url=" + i[1];
        cur4.execute(sql)
        conn.commit();
    return redirect("/")"""

@app.route('/add', methods=["POST"])
def add():
    Url = request.form.get("URL")
    id = request.form.get("id")
    time = datetime.datetime.today()
    sql = "insert into fund(number,url) values(" + id + "," + Url + ")"
    cur3 = conn.cursor()
    cur3.execute(sql)
    conn.commit()
    return redirect("/")


if __name__ == "__main__":
       app.run()

