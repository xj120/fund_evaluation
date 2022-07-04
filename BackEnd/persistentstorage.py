import datetime
import json
import time

import BackEnd.crawler

import pymysql


# 连接数据库
def linkDatabase():
    try:
        pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation',
                        charset='utf8')
    except:
        return None
    else:
        db = pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation',
                             charset='utf8')
        # print(type(db).__name__)
        return db


# 添加一个投资组合
def addPortfolio(portfolio):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        insert into portfolio(number,name, manager_name, url,found_date,max_drawdown,volatility,sharpe_rate,rate_per_ann,income_since_found,followers) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (portfolio.number, portfolio.name, portfolio.manager_name, portfolio.url, portfolio.found_date,
                 portfolio.max_drawdown, portfolio.volatility, portfolio.sharpe_rate,
                 portfolio.rate_per_ann, portfolio.income_since_found, portfolio.followers)
        cursor.execute(sql, param)
        db.commit()

        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 删除一个投资组合
def deletePortfolio(link):
    if len(link) != 38 and len(link) != 58:
        return False

    if len(link) == 38:
        number = link[30:38]
    elif len(link) == 58:
        number = link[32:39]

    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        delete from portfolio
        where number = %s
        '''
        param = (number)
        cursor.execute(sql, param)

        db.commit()

        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 添加一个投资组合的历史记录
def addHistoryRecord(records):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        for record in records:
            sql = '''
            insert into history_record(number,net_assert_value,daily_rise_drop,date)
            values(%s,%s,%s,%s)
            '''
            param = (record.number, record.net_assert_value, record.daily_rise_drop, record.date)
            cursor.execute(sql, param)
            db.commit()

        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 向数据库中插入调仓历史记录
def addRepositionRecord(repositions):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        for reposition in repositions:
            sql = '''
            insert into reposition_record(number,adjust_date,fund_code,proportion)
            values(%s,%s,%s,%s)
            '''
            for record in reposition.records:
                param = (reposition.number, reposition.adjust_date, record.get('fund_code'), record.get('percent'))
                cursor.execute(sql, param)
                db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 更新投资组合的历史记录
def updateRecord(link):
    try:
        links = getPortfolioList()
        if link in links:
            last_date = getLastDate(link)
            if last_date is None:
                span = 30000
            else:
                now_date = time.localtime(time.time())
                now_date = datetime.date(now_date[0], now_date[1], now_date[2])
                span = (now_date - last_date).days
                # print(span)

            records = BackEnd.crawler.getHistoryRecord(link, str(span))
            addHistoryRecord(records)
        return True
    except Exception as e:
        print(e)
        return False


# 更新投资组合的基本信息
def updatePortfolio(portfolio):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        update portfolio
        set max_drawdown = %s, volatility = %s, sharpe_rate = %s, rate_per_ann = %s, income_since_found = %s, followers = %s
        where number = %s
        '''
        param = (portfolio.max_drawdown, portfolio.volatility, portfolio.sharpe_rate,
                 portfolio.rate_per_ann, portfolio.income_since_found, portfolio.followers, portfolio.number)
        cursor.execute(sql, param)
        db.commit()

        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 得到投资组合历史记录的最后一天
def getLastDate(url):
    db = linkDatabase()
    cursor = db.cursor()
    if len(url) != 38 and len(url) != 58:
        return None

    if len(url) == 38:
        number = url[30:38]
    elif len(url) == 58:
        number = url[32:39]
    try:
        sql = '''
        select date
        from history_record
        where number = %s
        order by history_record.date desc LIMIT 0,1
        ''' % ('\"' + number + '\"')
        cursor.execute(sql)
        db.commit()
        record = cursor.fetchone()
        cursor.close()
        db.close()
        return record[0]
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 检查该url是否合法，再检查投资组合是否存在
def checkPortfolio(url):
    db = linkDatabase()
    cursor = db.cursor()
    if len(url) != 38 and len(url) != 58:
        return False

    if len(url) == 38:
        number = url[30:38]
    elif len(url) == 58:
        number = url[32:39]
    try:
        sql = '''
        select *
        from history_record
        where number = %s
        ''' % ('\"' + number + '\"')
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchone()
        if data is not None:
            cursor.close()
            db.close()
            return True
        else:
            cursor.close()
            db.close()
            return False
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 得到数据库内已有的投资组合列表
def getPortfolioList():
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select url
    from portfolio
    '''
    urls_list = []
    try:
        cursor.execute(sql)
        db.commit()
        links = cursor.fetchall()
        for link in links:
            urls_list.append(link[0])
        return urls_list
    except Exception as e:
        print(e)
        cursor.close()
        db.close()
        return None


# 得到URL和时间的信息，传给前端
def getUrlAndDateInfo():
    info_dict = {}
    portfolio_list = getPortfolioList()
    for f in portfolio_list:
        info_dict[f] = str(getLastDate(f))
    return info_dict


# 编写投资组合信息JSON文件给前端
def getTableJson():
    table = {"code": 0, "msg": ""}
    data = []
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select number, name, manager_name, income_since_found, max_drawdown, sharpe_rate, rate_per_ann, volatility, followers, reposition_level, average_holding_time
    from portfolio
    '''
    try:
        cursor.execute(sql)
        db.commit()
        portfolios = cursor.fetchall()
        for portfolio in portfolios:
            portfolio_dict = {"v_id": portfolio[0], "group_id": portfolio[1], "manager_name": portfolio[2],
                              "gains": portfolio[3], "max_retracement": portfolio[4],
                              "sharpe_ratio": portfolio[5], "rate_per_ann": portfolio[6],
                              "annualized_volatility": portfolio[7], "fans_num": portfolio[8],
                              "reposition_level": portfolio[9], "average_holding_time": portfolio[10]}
            data.append(portfolio_dict)
        table["data"] = data
        with open(file='.\\static\\data\\table.json', mode='w', encoding='utf-8') as f:
            t = json.dumps(table, ensure_ascii=False)
            f.write(t)
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


# 编写投资组合历史记录的JSON文件给前端
def getRecordJson():
    line = {}
    data = []
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select name, daily_rise_drop, date
    from portfolio,history_record
    where portfolio.number = history_record.number
    '''
    try:
        cursor.execute(sql)
        db.commit()
        records = cursor.fetchall()
        for record in records:
            if record[1] is None:
                record[1] = 0.0
            r_dict = {"name": record[0], "daily_rise_drop": record[1], "date": str(record[2])}
            data.append(r_dict)
        line["data"] = data
        with open(file='.\\static\\data\\line.json', mode='w', encoding='utf-8') as f:
            t = json.dumps(line, ensure_ascii=False)
            f.write(t)
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


if __name__ == '__main__':
    getTableJson()
    getRecordJson()
