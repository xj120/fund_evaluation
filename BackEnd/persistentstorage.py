import datetime
import json
import time

import BackEnd.crawler

import pymysql


def linkDatabase():
    try:
        pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation', charset='utf8')
    except:
        return None
    else:
        db = pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation',
                             charset='utf8')
        # print(type(db).__name__)
        return db


def addFund(fund):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        insert into fund(number,name,url,found_date,max_drawdown,volatility,sharpe_rate,rate_per_ann,income_since_found,followers) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (fund.number, fund.name, fund.url, fund.found_date,
                 fund.max_drawdown, fund.volatility, fund.sharpe_rate,
                 fund.rate_per_ann, fund.income_since_found, fund.followers)
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
        print('sb')
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


def updateRecord():
    try:
        links = getFundList()
        for link in links:
            last_date = getLastDate(link)
            if last_date is None:
                span = 30000
            else:
                now_date = time.localtime(time.time())
                now_date = datetime.date(now_date[0], now_date[1], now_date[2])
                span = (now_date - last_date).days
                print(span)

            records = BackEnd.crawler.getHistoryRecord(link, str(span))
            addHistoryRecord(records)
        return True
    except Exception as e:
        print(e)
        return False


def updateFund(fund):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        update fund
        set max_drawdown = %s, volatility = %s, sharpe_rate = %s, rate_per_ann = %s, income_since_found = %s, followers = %s
        where number = %s
        '''
        param = (fund.max_drawdown, fund.volatility, fund.sharpe_rate,
                 fund.rate_per_ann, fund.income_since_found, fund.followers, fund.number)
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
        '''%('\"'+number+'\"')
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


def checkFund(url):
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
        '''%('\"'+number+'\"')
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


def getFundList():
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select url
    from fund
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


def getUrlAndDateInfo():
    info_dict = {}
    fund_list = getFundList()
    for f in fund_list:
        info_dict[f] = str(getLastDate(f))
    return info_dict


def getTableJson():
    table = {"code": 0,"msg": ""}
    data = []
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select number, name, income_since_found, max_drawdown, sharpe_rate, volatility, followers
    from fund
    '''
    try:
        cursor.execute(sql)
        db.commit()
        funds = cursor.fetchall()
        for fund in funds:
            fund_dict = {"v_id": fund[0], "group_id": fund[1], "gains": fund[2], "max_retracement": fund[3],
                         "sharpe_ratio": fund[4], "annualized_volatility": fund[5], "fans_num": fund[6]}
            data.append(fund_dict)
        table["data"] = data
        with open(file='..\\static\\data\\table.json',mode='w',encoding='utf-8') as f:
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


def getRecordJson():
    line = {}
    data = []
    db = linkDatabase()
    cursor = db.cursor()
    sql = '''
    select name, daily_rise_drop, date
    from fund,history_record
    where fund.number = history_record.number
    '''
    try:
        cursor.execute(sql)
        db.commit()
        records = cursor.fetchall()
        for record in records:
            r_dict = {"name":record[0], "daily_rise_drop":record[1], "date":str(record[2])}
            data.append(r_dict)
        line["data"] = data
        with open(file='..\\static\\data\\line.json',mode='w',encoding='utf-8') as f:
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
    print(getUrlAndDateInfo())