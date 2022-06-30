import BackEnd.crawler as crawler
import BackEnd.persistentstorage as persistentstorage
import datetime
import json
import time
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


# 所有组合的的年化收益率的数学期望E(x)，E(X)=所有组合年收益率之和/组合数
def getIncomeEX():
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
        number = number + 1
        # 这里是因为且慢基金爬取的收益率没有百分号，所以将收益率大于二的全部除以100
        if row[0] > 2:
            a = row[0] / 100
        else:
            a = row[0]
        value1 = a + value1
    return round((value1 / number), 2)


# 所有组合的最大回撤的数学期望E(x)，E(X)=所有组合最大回撤之和除以总组合数
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
        if row[0] != None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)


# 粉丝数量的数学期望，E(X)=所有组合粉丝数之和除以总组合数
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
        if row[0] != None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)


# 计算收益与粉丝的E(XY)，E(XY)=所有组合年收益率与粉丝的乘积之和除以总组合数
def getIncomeEXY():
    db = linkDatabase()
    cursor = db.cursor()
    # 这里是因为且慢基金爬取的收益率没有百分号，所以将且慢和蛋卷的分开查找再合并
    sql1 = '''
        (SELECT *
         FROM (SELECT income_since_found*followers
            FROM portfolio
						where income_since_found<2)as d)UNION (SELECT *
         FROM (SELECT income_since_found*followers*0.01
            FROM portfolio
						where income_since_found>2)as d)
            '''
    cursor.execute(sql1)
    results2 = cursor.fetchall()
    value1 = 0
    number = 0
    for row in results2:
        if row[0] != None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)


# 计算最大回撤与粉丝的E(XY)，E(XY)=所有组合最大回撤与粉丝的乘积之和除以总组合数
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
        if row[0] != None:
            number = number + 1
            value1 = row[0] + value1
    return round((value1 / number), 2)


# 计算收益的Cov(X)，Cov(X)=E(XY)-E(X)E(Y)
def getIncomeCov():
    a = getIncomeEXY()
    b = getIncomeEX()
    c = getFollowersEX()
    d = a - b * c
    return d


# 计算最大回撤的Cov(X),Cov(X)=E(XY)-E(X)E(Y)
def getMaxDrawDownCov():
    a = getMaxDrawDownEXY()
    b = getMaxDrawDownEX()
    c = getFollowersEX()
    d = a - b * c
    return d


# 计算收益的D(X)的平方根，其中D(X)=E(X^2)-E(X)*E(X)
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
        number = number + 1
        # 这里是因为且慢基金爬取的收益率没有百分号，所以将收益率大于二的全部除以100
        if row[0] > 2:
            a = row[0] / 100
        else:
            a = row[0]
        value1 = a * a + value1
    # D(X)的平方根
    b = getIncomeEX()
    a = round((value1 / number), 2) - b * b
    return round(pow(a, 0.5), 4)


# 计算最大回撤的D(X)的平方根，其中D(X)=E(X^2)-E(X)*E(X)
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
        if row[0] != None:
            number = number + 1
            value1 = row[0] * row[0] + value1
    # D(X)的平方
    b = getMaxDrawDownEX()
    a = round((value1 / number), 2) - b * b
    return round(pow(a, 0.5), 4)


# 计算粉丝的D(X)的平方根，其中D(X)=E(X^2)-E(X)*E(X)
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
        if row[0] != None:
            number = number + 1
            value1 = row[0] * row[0] + value1
    # D(X)的平方
    b = getFollowersEX()
    a = round((value1 / number), 2) - b * b

    c = round(pow(a, 0.5), 4)
    return c


######   调用函数请看下面     #########

# 一键计算收益与粉丝的相关系数，相关系数=Cov(X)除以粉丝的D(Y)的平方根与收益率的D(X)的平方根
def getIncomeCalculation():
    a = getIncomeCov()
    b = getIncomeDX()
    c = getFollowersDX()
    d = round((a / c / b), 2)
    return d


# 一键计算最大回撤与粉丝的相关系数,相关系数=Cov(X)除以粉丝的D(Y)的平方根与最大回撤的D(X)的平方根
def getMaxDrawDownCalculation():
    a = getMaxDrawDownCov()
    b = getMaxDrawDownDX()
    c = getFollowersDX()
    d = round((a / c / b), 2)
    return d


# 返回计算过程
def getIncomeProcedure():
    a = '''计算过程 (X: 年化收益率 , Y: 粉丝) :
     
E(X) = X1 * p(X1) + X2 * p(X2) + …… + Xn * p(Xn) = ''' + str(getIncomeEX()) + '''

E(Y) = X1 * p(X1) + X2 * p(X2) + …… + Xn * p(Xn) = ''' + str(getFollowersEX()) + '''

E(XY) = XY1 * p(XY1) + XY2 * p(XY2) + …… + XYn * p(XYn) = ''' + str(getIncomeEXY()) + '''

Cov(X) = E(XY) - E(X) * E(Y) = ''' + str(getIncomeCov()) + '''

√D(X) = √(E(X^2) - E(X) * E(X)) = ''' + str(getIncomeDX()) + '''

√D(Y) = √(E(X^2) - E(X) * E(X)) = ''' + str(getFollowersDX()) + '''

r = Cov(X) / (√D(X) * √D(Y)) = ''' + str(getIncomeCalculation()) + ''''''
    return a


def getMaxDrawDownProcedure():
    a = '''计算过程 (X: 最大回撤 , Y: 粉丝) : 
    
E(X) = X1 * p(X1) + X2 * p(X2) + …… + Xn * p(Xn) = ''' + str(getMaxDrawDownEX()) + '''

E(Y) = X1 * p(X1) + X2 * p(X2) + …… + Xn * p(Xn) = ''' + str(getFollowersEX()) + '''

E(XY) = XY1*p(XY1) + XY2 * p(XY2) + …… + XYn * p(XYn) = ''' + str(getMaxDrawDownEXY()) + '''

Cov(X) = E(XY) - E(X) * E(Y) = ''' + str(getMaxDrawDownCov()) + '''

√D(X) = √(E(X^2) - E(X) * E(X)) = ''' + str(getMaxDrawDownDX()) + '''

√D(Y) = √(E(X^2) - E(X) * E(X)) = ''' + str(getFollowersDX()) + '''

r = Cov(X) / (√D(X) * √D(Y)) = ''' + str(getMaxDrawDownCalculation()) + ''''''
    return a


if __name__ == '__main__':
    a = "CSI1006"
    b = "161005"
    c = "2018-09-27"
    # print(getPortfolioFollows("CSI1033"))
    # getStore()
    # print(getIncomeEX())
    # print(getFollowersEX())
    # print(getIncomeEXY())
    # print(getIncomeCov())
    # print(getIncomeDX())
    # print(getFollowersDX())
    # print(getIncomeCalculation())
    #
    # print(getMaxDrawDownEX())
    # print(getFollowersEX())
    # print(getMaxDrawDownEXY())
    # print(getMaxDrawDownCov())
    # print(getMaxDrawDownDX())
    # print(getFollowersDX())
    # print(getMaxDrawDownCalculation())
    # print(getIncomeProcedure())
    print(getMaxDrawDownProcedure())
