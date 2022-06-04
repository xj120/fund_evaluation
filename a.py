from flask import Flask, render_template, request
import pymysql
from werkzeug.utils import redirect
import BackEnd.crawler
import time



app = Flask(__name__)

#数据库信息
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='danjuan',
    charset='utf8'
)
app.debug = True


@app.route('/')
def index2():
    cur = conn.cursor()
    sql = "select * from student"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template("index.html", content = content)

@app.route('/delete/<i>')
def delete(i):
   sql = "delete from student where id =" + i[1]
   cur2 = conn.cursor()
   cur2.execute(sql)
   conn.commit()
   return redirect("/")

#爬取一个URL，i[1]是URL
@app.route('/spide/<i>')
def spid(i):
 BackEnd.crawler.getFundInfo(i[1])
 cur4 = conn.cursor()
 sql="update student  set name=" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) +"where id=" + i[1];
 cur4.execute(sql)
 conn.commit();
 return redirect("/")

#爬取全部URL，content是全部记录，i是单条记录，i[1]是URL
@app.route('/spidall/<content>')
def spidall(content):
    for i in content:
        BackEnd.crawler.getFundInfo(i[1])
        cur4 = conn.cursor()
        sql = "update student  set name=" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "where id=" + i[1];
        cur4.execute(sql)
        conn.commit();
    return redirect("/")

@app.route('/add', methods=["POST"])
def add():
    url = request.form.get("URL")
    sql = "insert into student values(" + url +", '数据未爬取')"
    cur3 = conn.cursor()
    cur3.execute(sql)
    conn.commit()
    return redirect("/")


if __name__ == "__main__":
       app.run()

