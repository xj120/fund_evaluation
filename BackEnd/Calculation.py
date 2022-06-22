import BackEnd.crawler as crawler
import BackEnd.persistentstorage as persistentstorage
import datetime
import json
import time
from BackEnd import a
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




#所有组合的的年收益率的数学期望E(x)
def getIncomeEX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1='''
    SELECT income_since_found
        FROM portfolio
        '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1=0
    number=0
    for row in results2:
        if row[0]<2:
            number=number+1
            value1 = row[0]+value1
    return round((value1/number),2)


#所有组合的最大回撤的数学期望E(x)
def getMaxDrawDownEX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
        SELECT max_drawdown
            FROM portfolio
            '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] < 2:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)

#所有组合的市值的数学期望E(x)
def getSHIZHIEX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
        SELECT income_since_found
            FROM portfolio
            '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] < 2:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)

#粉丝数量的数学期望
def getFollowersEX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
        SELECT followers
            FROM portfolio
            '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0]!=None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)




#计算收益与粉丝的E(XY)
def getIncomeEXY():
    db = linkDatabase()
    cursor = db.cursor()
    sql1 = '''
        SELECT income_since_found*followers
            FROM portfolio
            '''
    cursor.execute(sql1)
    results2 = cursor.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0]!=None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)

#计算最大回撤与粉丝的E(XY)
def getMaxDrawDownEXY():
    db = linkDatabase()
    cursor = db.cursor()
    sql1 = '''
        SELECT max_drawdown*followers
            FROM portfolio
            '''
    cursor.execute(sql1)
    results2 = cursor.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0]!=None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)

#计算市值与粉丝的E(XY)
def getSHIZHIEXY():
    db = linkDatabase()
    cursor = db.cursor()
    sql1 = '''
        SELECT income_since_found*followers
            FROM portfolio
            '''
    cursor.execute(sql1)
    results2 = cursor.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0]!=None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)



#计算收益的Cov(X)
def getIncomeCov():
    a=getIncomeEXY()
    b=getIncomeEX()
    c=getFollowersEX()
    d=a-b*c
    return d

#计算最大回撤的Cov(X)
def getMaxDrawDownCov():
    a=getMaxDrawDownEXY()
    b=getMaxDrawDownEX()
    c=getFollowersEX()
    d=a-b*c
    return d

#计算市值的Cov(X)
def getSHIZHICov():
    a=getSHIZHIEXY()
    b=getSHIZHIEX()
    c=getFollowersEX()
    d=a-b*c
    return d


#计算收益的D(X)的平方根
def getIncomeDX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT income_since_found
           FROM portfolio
           '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] < 2:
            number = number + 1
            value1 = row[0]*row[0] + value1
    #D(X)的平方
    b=getIncomeEX()
    a=round((value1 / number), 2)-b*b
    return pow(a,0.5)


#计算最大回撤的D(X)的平方根
def getMaxDrawDownDX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT max_drawdown
           FROM portfolio
           '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0]!=None:
            number = number + 1
            value1 = row[0]*row[0] + value1
    #D(X)的平方
    b=getMaxDrawDownEX()
    a=round((value1 / number), 2)-b*b
    return pow(a,0.5)


#计算市值的D(X)的平方根
def getSHIZHIDX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT income_since_found
           FROM portfolio
           '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] < 2:
            number = number + 1
            value1 = row[0]*row[0] + value1
    #D(X)的平方
    b=getIncomeEX()
    a=round((value1 / number), 2)-b*b
    return pow(a,0.5)

#计算粉丝的D(X)的平方根
def getFollowersDX():
    db = linkDatabase()
    cursor2 = db.cursor()
    sql1 = '''
       SELECT followers
           FROM portfolio
           '''
    cursor2.execute(sql1)
    results2 = cursor2.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] !=None:
            number = number + 1
            value1 = row[0]*row[0] + value1
    #D(X)的平方
    b=getFollowersEX()
    a=round((value1 / number), 2)-b*b

    c=pow(a,0.5)
    return c


#收益相关系数
def getIncomeCalculation():
    a=getIncomeCov()
    b=getIncomeDX()
    c=getFollowersDX()
    d=round((a/c/b),2)
    return d
#最大回撤相关系数
def getMaxDrawDownCalculation():
    a=getMaxDrawDownCov()
    b=getMaxDrawDownDX()
    c=getFollowersDX()
    d=round((a/c/b),2)
    return d
#市值相关系数
def getSHIZHICalculation():
    a=getSHIZHICov()
    b=getSHIZHIDX()
    c=getFollowersDX()
    d=round((a/c/b),2)
    return d

if __name__ == '__main__':
    a = "CSI1006"
    b="161005"
    c="2018-09-27"
    #print(getPortfolioFollows("CSI1033"))
    #getStore()
    print(getIncomeCalculation())