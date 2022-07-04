import json

from flask import Flask, render_template, request
from werkzeug.utils import redirect

import BackEnd.persistentstorage as persistentstorage
import BackEnd.crawler as crawler
import BackEnd.reposition_level as reposition_level
import BackEnd.holdingtime as holdingtime
from BackEnd import Calculation

app = Flask(__name__)


@app.route('/FundEvaluation', methods=['GET', 'POST'])
def index():  # 基金评比页面的渲染 TODO
    c1 = Calculation.getIncomeProcedure()
    c2 = Calculation.getMaxDrawDownProcedure()
    r1 = Calculation.getIncomeCalculation()
    r2 = Calculation.getMaxDrawDownCalculation()
    return render_template("FundEvaluation.html", r1=r1, r2=r2, c1=c1, c2=c2)


@app.route('/')
def mainPage():  # 主页的渲染
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
def index2():  # URL管理界面的渲染
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


@app.route('/spide', methods=["POST"])
def spide():
    # 爬虫程序：
    link = request.form.get('url')
    if persistentstorage.checkPortfolio(link):
        f = crawler.getPortfolioInfo(link)
        persistentstorage.updatePortfolio(f)
        persistentstorage.updateRecord(link)
        d = crawler.getRepositionRecord(link)
        persistentstorage.addRepositionRecord(d)
    else:
        f = crawler.getPortfolioInfo(link)
        persistentstorage.addPortfolio(f)
        r = crawler.getHistoryRecord(link, '30000')
        persistentstorage.addHistoryRecord(r)
        d = crawler.getRepositionRecord(link)
        persistentstorage.addRepositionRecord(d)
        holdingtime.getHoldTimeSingleStore(link)
        reposition_level.getRepositionLevelSingleStore(link)

    persistentstorage.getTableJson()
    persistentstorage.getRecordJson()

    return redirect('/')


@app.route('/delete', methods=["POST"])
def delete():
    link = request.form.get('url2')
    # 删除
    persistentstorage.deletePortfolio(link)

    persistentstorage.getTableJson()
    persistentstorage.getRecordJson()
    return redirect('/')


@app.route('/testAjax/s_year=<s_year>&s_month=<s_month>&s_day=<s_day>&e_year=<e_year>&e_month=<e_month>&e_day=<e_day>',
           methods=["GET"])
def test(s_year, s_month, s_day, e_year, e_month, e_day):
    start = s_year + '-' + s_month + '-' + s_day
    end = e_year + '-' + e_month + '-' + e_day
    # +++++++++++
    reply = {'success': 'true'}
    return json.dumps(reply)


@app.route('/redrawLine')
def redrawLine():
    reply = {"data": [{"name": "巨人指数", "daily_rise_drop": 0, "date": "2016-05-30"},
                      {"name": "巨人指数", "daily_rise_drop": 0.226044, "date": "2016-06-30"}]}
    return json.dumps(reply)


@app.route('/redrawTable')
def redrawTable():
    reply = {"code": 0, "msg": "", "data": [
        {"v_id": "ZH000193", "group_id": "巨人指数", "manager_name": "盈米基金", "gains": 46.01, "max_retracement": 36.05,
         "sharpe_ratio": 0.26, "rate_per_ann": 6.43, "annualized_volatility": 16.81, "fans_num": 29463,
         "reposition_level": 0.52, "average_holding_time": 18.0},
    ]}
    return json.dumps(reply)


if __name__ == '__main__':
    app.run()
