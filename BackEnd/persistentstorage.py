import pymysql


def linkDatabase():
    try:
        pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation', charset='utf8')
    except:
        return False
    else:
        db = pymysql.connect(host='localhost', user='root', password='a8700998', db='portfolio_evaluation',
                             charset='utf8')
        return db


def addFund(fund):
    db = linkDatabase()
    cursor = db.cursor()
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

def addHistoryRecord(records):
    db = linkDatabase()
    cursor = db.cursor()
    for record in records:
        sql = '''
        insert into history_record(number,net_assert_value,daily_rise_drop,date)
        values(%s,%s,%s,%s)
        '''
        param = (record.number,record.net_assert_value,record.daily_rise_drop,record.date)
        cursor.execute(sql, param)
        db.commit()

    cursor.close()
    db.close()
