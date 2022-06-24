from flask import Flask, render_template, request
from werkzeug.utils import redirect

import BackEnd.persistentstorage as persistentstorage
import BackEnd.crawler as crawler

app = Flask(__name__)


@app.route('/FundEvaluation', methods=['GET', 'POST'])
def index():
    test = '!!!!!'
    ab = '??????'
    return render_template("FundEvaluation.html", test=test, ab=ab)


@app.route('/')
def mainPage():
    return render_template("MainPage.html")


"""#数据库信息
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='Portfolio_Evaluation',
    charset='utf8'
)"""
app.debug = True


@app.route('/url')
def index2():
    content = persistentstorage.getUrlAndDateInfo()
    # content：url的字典
    return render_template("index.html", content=content)


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
    # 爬虫程序：
    link = request.form.get('url')
    if persistentstorage.checkPortfolio(link):
        f = crawler.getPortfolioInfo(link)
        persistentstorage.updatePortfolio(f)
        persistentstorage.updateRecord(link)
    else:
        f = crawler.getPortfolioInfo(link)
        persistentstorage.addPortfolio(f)
        r = crawler.getHistoryRecord(link, '30000')
        persistentstorage.addHistoryRecord(r)

    persistentstorage.getTableJson()
    persistentstorage.getRecordJson()

    return redirect('/')

@app.route('/delete',methods=["POST"])
def delete():
    link = request.form.get('url2')
    #删除

    return redirect('/')



if __name__ == '__main__':
    app.run()
