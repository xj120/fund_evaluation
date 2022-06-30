from flask import Flask, render_template, request
from werkzeug.utils import redirect

import BackEnd.persistentstorage as persistentstorage
import BackEnd.crawler as crawler
import BackEnd.Calculation as Calculation


app = Flask(__name__)


@app.route('/FundEvaluation', methods=['GET', 'POST'])
def index():
    c1 = Calculation.getIncomeProcedure()
    c2 = Calculation.getMaxDrawDownProcedure()
    r1 = Calculation.getIncomeCalculation()
    r2 = Calculation.getMaxDrawDownCalculation()
    return render_template("FundEvaluation.html", r1=r1, r2=r2, c1=c1, c2=c2)


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
    crawler.updateXsign()
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


@app.route('/delete', methods=["POST"])
def delete():
    link = request.form.get('url2')
    #删除
    persistentstorage.deletePortfolio(link)

    persistentstorage.getTableJson()
    persistentstorage.getRecordJson()
    return redirect('/')



if __name__ == '__main__':
    app.run()