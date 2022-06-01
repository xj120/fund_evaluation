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
        print(e)
        db.rollback()
        cursor.close()
        db.close()
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


def getLastDate(number):
    db = linkDatabase()
    cursor = db.cursor()
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

