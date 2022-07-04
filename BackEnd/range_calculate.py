import datetime
import json
import time

import BackEnd.crawler
import app

import pymysql
import math
import numpy


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


# 计算年化波动率
def calculateVolatility(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        select *
        from history_record
        where date < %s and date > %s
        '''
        param = (end_date, start_date)
        cursor.execute(sql, param)
        db.commit()
        records = cursor.fetchall()
        # print(records)
        # 对数日收益率
        diffs = []
        diffs_group = []
        numbers = []
        for i in range(len(records) - 1):
            if records[i][0] == records[i + 1][0]:
                diffs_group.append(math.log(records[i + 1][1] / records[i][1]))
            else:
                diffs.append(diffs_group)
                diffs_group = []
                numbers.append(records[i][0])
        diffs.append(diffs_group)
        numbers.append(records[len(records) - 1][0])
        # print(diffs)
        # print(numbers)
        # 标准差
        year_volatility_list = []
        for diff in diffs:
            standard_deviation = numpy.std(diff)
            year_volatility = standard_deviation * math.sqrt(242)
            year_volatility_list.append(year_volatility)
        # print(year_volatility_list)
        year_volatility_dict = []
        for i in range(len(numbers)):
            year_volatility_dict.append(
                {'number': numbers[i], 'year_volatility': round(year_volatility_list[i] * 100, 2)})
        # print(year_volatility_dict)
        db.close()
        cursor.close()

        # range_volatility = {"data": year_volatility_list}
        # with open(file='..\\static\\data\\range_volatility.json', mode='w', encoding='utf-8') as f:
        #     t = json.dumps(range_volatility, ensure_ascii=False)
        #     f.write(t)

        return year_volatility_dict
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 计算最大回撤
def calculateMaxDrawdown(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
            select number, net_assert_value, date
            from history_record
            where date < %s and date > %s
            '''
        param = (end_date, start_date)
        cursor.execute(sql, param)
        db.commit()
        records = cursor.fetchall()
        number_list = []
        # print(records)
        for record in records:
            number_list.append(record[0])
        number_list = list(set(number_list))
        # print(number_list)
        maxDrawdown_list = []
        maxDrawdown_dict = {}
        for number in number_list:
            nat_list = []
            for record in records:
                if number == record[0]:
                    nat_list.append(record[1])
            # print(nat_list)
            i = numpy.argmax((numpy.maximum.accumulate(nat_list) - nat_list) / numpy.maximum.accumulate(nat_list))
            if i == 0:
                maxDrawdown_dict['number'] = number
                maxDrawdown_dict['maxDrawdown'] = 0
                maxDrawdown_list.append(maxDrawdown_dict)
            else:
                j = numpy.argmax(nat_list[:i])
                maxDrawdown_dict['number'] = number
                maxDrawdown_dict['maxDrawdown'] = round((nat_list[j] - nat_list[i]) / (nat_list[j]) * 100, 2)
                maxDrawdown_list.append(maxDrawdown_dict.copy())

        # range_maxDrawdown = {"data": maxDrawdown_list}
        # with open(file='..\\static\\data\\range_maxDrawdown.json', mode='w', encoding='utf-8') as f:
        #     t = json.dumps(range_maxDrawdown, ensure_ascii=False)
        #     f.write(t)

        db.close()
        cursor.close()
        return maxDrawdown_list
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 计算夏普率
def calculateSharpRate(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        no_risk_rate = 1.5
        ann_list = calculateAnnualizeRate(start_date, end_date)
        vol_list = calculateVolatility(start_date, end_date)
        sharpe_list = []
        sharpe_dict = {}
        for i in range(len(ann_list)):
            sharpe = (ann_list[i].get('ann_rate') - no_risk_rate) / vol_list[i].get('year_volatility')
            sharpe_dict['number'] = ann_list[i].get('number')
            sharpe_dict['sharpe_rate'] = round(sharpe, 2)
            sharpe_list.append(sharpe_dict.copy())

        # range_sharpe = {"data": sharpe_list}
        # with open(file='..\\static\\data\\range_sharpe.json', mode='w', encoding='utf-8') as f:
        #     t = json.dumps(range_sharpe, ensure_ascii=False)
        #     f.write(t)

        db.close()
        cursor.close()
        return sharpe_list
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 计算年化收益率
def calculateAnnualizeRate(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
            select number, avg(daily_rise_drop) as avg_rise
            from history_record
            where date < %s and date > %s
            group by number
           '''
        param = (end_date, start_date)
        cursor.execute(sql, param)
        db.commit()
        avg_records = cursor.fetchall()
        # print(avg_records)

        # sql = '''
        # select *
        # from history_record
        # where date < %s and date > %s
        # '''
        # param = (end_date, start_date)
        # cursor.execute(sql, param)
        # db.commit()
        # rise = []
        # rise_group = []
        # numbers = []
        # records = cursor.fetchall()
        # for i in range(len(records)-1):
        #     if records[i][0] == records[i+1][0]:
        #         rise_group.append((records[i+1][1]-records[i][1])/records[i][1])
        #     else:
        #         rise.append(rise_group)
        #         rise_group = []
        #         numbers.append(records[i][0])
        # rise.append(rise_group)
        # numbers.append(records[len(records)-1][0])
        # print(rise)
        # 标准差
        ann_rate = []
        for i in range(len(avg_records)):
            # standard_deviation = numpy.std(rise[i])
            ann_rate.append(round(avg_records[i][1] * 242, 2))
        # print(ann_rate)
        ann_list = []
        ann_dict = {}
        for i in range(len(avg_records)):
            ann_dict['number'] = avg_records[i][0]
            ann_dict['ann_rate'] = ann_rate[i]
            ann_list.append(ann_dict.copy())

        # range_ann = {"data": ann_list}
        # with open(file='..\\static\\data\\range_ann.json', mode='w', encoding='utf-8') as f:
        #     t = json.dumps(range_ann, ensure_ascii=False)
        #     f.write(t)

        db.close()
        cursor.close()
        return ann_list
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 计算区间涨幅
def calculateRangeRise(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
                select *
                from history_record
                where date < %s and date > %s
                GROUP BY number;
              '''
        param = (end_date, start_date)
        cursor.execute(sql, param)
        db.commit()
        start_records = cursor.fetchall()
        # print(start_records)

        sql = '''
                with his_rec as
                (
                SELECT *
                from history_record
                where date < %s and date > %s
                )
                select a.*
                from his_rec as a left join his_rec as b
                on a.number = b.number and a.date < b.date
                where b.date is null
             '''
        param = (end_date, start_date)
        cursor.execute(sql, param)
        db.commit()
        end_records = cursor.fetchall()
        # print(end_records)

        range_rise_dict = {}
        range_rise_list = []

        for i in range(len(start_records)):
            for j in range(len(end_records)):
                if start_records[i][0] == end_records[j][0]:
                    range_rise_dict['number'] = start_records[i][0]
                    range_rise_dict['rise'] = round(
                        (end_records[j][1] - start_records[i][1]) / start_records[i][1] * 100, 2)
                    range_rise_list.append(range_rise_dict.copy())

        # range_rise = {"data": range_rise_list}
        # with open(file='..\\static\\data\\range_rise.json', mode='w', encoding='utf-8') as f:
        #     t = json.dumps(range_rise, ensure_ascii=False)
        #     f.write(t)

        db.close()
        cursor.close()
        return range_rise_list
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return None


# 将计算结果整合起来哦
def accumulateRangeCalculation(start_date, end_date):
    db = linkDatabase()
    cursor = db.cursor()
    try:
        sql = '''
        select number, name, manager_name, followers, reposition_level, average_holding_time
        from portfolio
        '''
        cursor.execute(sql)
        name_tuple = cursor.fetchall()
        print(name_tuple)
        range_vol_list = calculateVolatility(start_date, end_date)
        range_md_list = calculateMaxDrawdown(start_date, end_date)
        range_rise_list = calculateRangeRise(start_date, end_date)
        range_ann_list = calculateAnnualizeRate(start_date, end_date)
        range_sharpe_list = calculateSharpRate(start_date, end_date)
        number_list = []
        cal_list = []
        cal_dict = {}
        for each_dict in range_sharpe_list:
            number_list.append(each_dict.get('number'))
        for number in number_list:
            cal_dict['v_id'] = number
            for name in name_tuple:
                if name[0] == number:
                    cal_dict['group_id'] = name[1]
                    cal_dict['manager_name'] = name[2]
                    cal_dict['fans_num'] = name[3]
                    cal_dict['reposition_level'] = name[4]
                    cal_dict['average_holding_time'] = name[5]
                    break
            for vol in range_vol_list:
                if vol.get('number') == number:
                    cal_dict['annualized_volatility'] = vol.get('year_volatility')
                    break
            for md in range_md_list:
                if md.get('number') == number:
                    cal_dict['max_retracement'] = md.get('maxDrawdown')
                    break
            for rise in range_rise_list:
                if rise.get('number') == number:
                    cal_dict['gains'] = rise.get('rise')
                    break
            for ann in range_ann_list:
                if ann.get('number') == number:
                    cal_dict['rate_per_ann'] = ann.get('ann_rate')
            for sharpe in range_sharpe_list:
                if sharpe.get('number') == number:
                    cal_dict['sharpe_ratio'] = sharpe.get('sharpe_rate')
            cal_list.append(cal_dict.copy())
        n = {'code': 0, 'msg': "", 'data': cal_list}
        app.new_table = json.dumps(n, ensure_ascii=False)
        db.close()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return False


if __name__ == '__main__':
    # print(calculateVolatility('2017-01-01', '2022-07-02'))
    # print(calculateMaxDrawdown('2017-01-01', '2022-07-02'))
    # print(calculateRangeRise('2017-01-01', '2022-07-02'))
    # print(calculateAnnualizeRate('2017-01-01', '2022-07-02'))
    # print(calculateSharpRate('2017-01-01', '2022-07-02'))
    accumulateRangeCalculation('2017-1-1', '2022-7-2')
