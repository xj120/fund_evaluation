import BackEnd.crawler as crawler
import BackEnd.persistentstorage as persistentstorage
import datetime
import json
import time
import pymysql


# 连接数据库
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


# 某个组合的涨幅
def getPortfolioUP(numbers, date):
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    value1 = 0
    value2 = 0
    sql1 = '''
    SELECT net_assert_value
        FROM history_record
        where number=
        ''' + "\'" + numbers + "\'" + "and date=" + "\'" + str(date) + "\'" + '''
        '''
    try:
        cursor2.execute(sql1)
        results2 = cursor2.fetchall()
        for row in results2:
            value1 = row[0]
        # 最后一天的价值
        sql2 = '''
            SELECT net_assert_value
                FROM history_record
                where number=
                ''' + "\'" + numbers + "\'" '''
                ORDER BY date DESC
                LIMIT 1
                '''
        cursor.execute(sql2)
        results = cursor.fetchall()
        for row in results:
            value2 = row[0]
        m = value2 - value1
        cursor.close()
        cursor2.close()
        return m
    except Exception as e:
        print(e)


# 单个基金调仓情况
def getMoveState(numbers, fund):
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT adjust_date
           from reposition_record
           where number=
           ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund + "\'" + '''
           and proportion=0
           and number like "Z%"
           limit 1
           '''
    sql2 = '''
           SELECT max(proportion)
               from reposition_record
               where number=
               ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund + "\'" + '''
                and number in(SELECT number
                FROM reposition_record
                where number like "Z%" and proportion=0
                group by number)
               '''
    try:
        cursor.execute(sql2)
        results = cursor.fetchall()
        proportion = 0
        for row2 in results:
            if row2[0] is not None:
                proportion = row2[0]
                if proportion > 1:
                    proportion = proportion / 100
        cursor2.execute(sql1)
        results2 = cursor2.fetchall()
        for row in results2:
            date = row[0]
            # 在这里令a等于基金的涨幅函数就可以了
            if crawler.getFundRise(fund, date) is not None:
                a = crawler.getFundRise(fund, date) / 100 * proportion
                b = getPortfolioUP(numbers, date)
                print(proportion)
                if b > a:
                    cursor.close()
                    cursor2.close()
                    return 1
                else:
                    cursor.close()
                    cursor2.close()
                    return 0
        cursor.close()
        cursor2.close()
        return 0
    except Exception as e:
        print(e)


# 某个组合的调仓成功次数
def getMoveSuccessTimes(numbers):
    db = linkDatabase()
    cursor = db.cursor()
    sql2 = '''
           select fund_code
           from reposition_record
           where number=
           ''' + "\'" + numbers + "\'" + '''
           group by fund_code
           '''
    try:
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        m = 0
        for row in results2:
            m = m + getMoveState(numbers, row[0])
            cursor.close()
        return m
    except Exception as e:
        print(e)


# 某个组合调仓总次数
def getMoveTimes(numbers):
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT proportion
           from reposition_record
           where number=
           ''' + "\'" + numbers + "\'"  '''
           '''

    try:
        cursor2.execute(sql1)
        results2 = cursor2.fetchall()
        m = 0
        for row in results2:
            proportion = row[0]
            if proportion == 0:
                m = m + 1
        cursor2.close()
        return m
    except Exception as e:
        print(e)


# 调仓成功率，即调仓水平
def getLevel(numbers):
    try:
        a = getMoveTimes(numbers)
        b = getMoveSuccessTimes(numbers)
        print("movetimes:",a)
        print("successtimes:",b)
        if a == 0:
            return 0
        else:
            return b / a
    except Exception as e:
        print(e)


# 将组合调仓水平存入数据库
def getStore():
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql1 = '''
               select number
               from reposition_record
               group by number
               '''
    # 组合
    try:
        cursor.execute(sql1)
        results2 = cursor.fetchall()

        for row in results2:
            sql2 = '''
                        update portfolio
                        set reposition_level = ''' + str(round(getLevel(row[0]), 2)) + '''
                        where number=''' + "\'" + row[0] + "\'"
            cursor2.execute(sql2)
            db.commit()
            cursor.close()
            cursor2.close()
            db.close()
    except Exception as e:
        print(e)


def getURLNumber(url):
    try:
        if len(url) == 38:
            number = url[30:38]
        return number
    except Exception as e:
        print(e)


#传入单个组合的url，即可将其调仓水平存入数据库
def getRepositionLevelSingleStore(url):
    try:
        number = getURLNumber(url)
        db = linkDatabase()
        cursor = db.cursor()
        cursor2 = db.cursor()

        sql2 = '''
                update portfolio
                 set reposition_level = ''' + str(round(getLevel(number), 2)) + '''
                 where number=''' + "\'" + number + "\'"
        cursor2.execute(sql2)
        db.commit()
        cursor.close()
        cursor2.close()
        db.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    a = "ZH000193"
    b = "000509"
    c = "2018-09-27"
    # print(getMoveSuccessTimes("CSI1033"))

    # print(getPortfolioUP(a,b))
    # print(getMoveTimes(a))
    # print(getMoveState(a,b))
    getRepositionLevelSingleStore('https://qieman.com/portfolios/ZH009664')