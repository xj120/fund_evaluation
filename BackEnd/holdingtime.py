import BackEnd.crawler as crawler
import BackEnd.persistentstorage as persistentstorage
import datetime
import json
import time

import BackEnd.crawler

import pymysql


# 连接数据库
def linkDatabase():
    try:
        pymysql.connect(host='localhost', user='root', password='111111', db='portfolio_evaluation', charset='utf8')
    except:
        return None
    else:
        db = pymysql.connect(host='localhost', user='root', password='111111', db='portfolio_evaluation',
                             charset='utf8')
        # print(type(db).__name__)
        return db


# 某个组合的某个基金持有时间
def getFundHoldingTime(numbers, fund_code):
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql1 = '''
    SELECT proportion
        from reposition_record
        where number=
        ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund_code + "\'" + '''
        ORDER BY adjust_date DESC
        LIMIT 1
        '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    for row in results2:
        proportion = row[0]
        if proportion == 0:
            sql2 = '''
                SELECT datediff(
                    (select adjust_date
                    from reposition_record
                    where number=
                    ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund_code + "\'" + '''
                    ORDER BY adjust_date DESC
                    LIMIT 1),
                    (select adjust_date
                    from reposition_record
                    where number=\
                    ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund_code + "\'" + '''
                    LIMIT 1)) as DuringTime 
                    '''

        else:
            sql2 = '''
                            SELECT datediff(
                                (select curdate()),
                                (select adjust_date
                                from reposition_record
                                where number=\
                                ''' + "\'" + numbers + "\'" + "and fund_code=" + "\'" + fund_code + "\'" + '''
                                LIMIT 1)) as DuringTime 
                                '''
    cursor.execute(sql2)
    results = cursor.fetchall()
    for row in results:
        duringtime = row[0]
        return duringtime


# 某个组合的所有基金平均持有时间
def getFund(numbers):
    db = linkDatabase()
    cursor = db.cursor()
    sql2 = '''
           select fund_code
           from reposition_record
           where number=
           ''' + "\'" + numbers + "\'" + '''
           group by fund_code
           '''
    cursor.execute(sql2)
    results = cursor.rowcount
    results2 = cursor.fetchall()
    m = 0
    i = 0
    for row in results2:
        fundlist = row[0]
        m = m + getFundHoldingTime(numbers, fundlist)
    return m / results / 30


# 将组合的平均持有时间存入数据库
def getStore():
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql1 = '''
               select number
               from reposition_record
               group by number
               '''
    cursor.execute(sql1)

    results2 = cursor.fetchall()

    for row in results2:
        row[0]
        sql2 = '''
                    update portfolio
                    set average_holding_time = ''' + str(round(getFund(row[0]))) + '''
                    where number=''' + "\'" + row[0] + "\'"
        cursor2.execute(sql2)
        db.commit()

def getURLNumber(url):
    if len(url)==38:
        number=url[30:38]
    return number
#传入单个组合的url，即可将其基金平均持有时间存入数据库
def getHoldTimeSingleStore(url):
    number=getURLNumber(url)
    db = linkDatabase()
    cursor = db.cursor()
    cursor2 = db.cursor()
    sql2 = '''
                       update portfolio
                       set average_holding_time = ''' + str(round(getFund(number))) + '''
                       where number=''' + "\'" + number + "\'"
    cursor2.execute(sql2)
    db.commit()



if __name__ == '__main__':
    a = "CSI1006"
    b = "161005"
    getSingleStore('https://qieman.com/portfolios/ZH000193')
    # print(persistentstorage.getPortfolioList())
