import json
import time

import requests
from seleniumwire import webdriver

import fund
import record

qm_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'x-sign': '165424501467009D30CFCCDB475FA9F196B651A85A6CE'
}

dj_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

def getXsign():
    driver = webdriver.Chrome()
    driver.get('https://qieman.com')


def getFundInfo(url):
    if len(url) != 38 and len(url) != 58:
        return None

    if len(url) == 38:
        number = url[30:38]
        return getFundInfo_qieman(number)
    elif len(url) == 58:
        number = url[32:39]
        return getFundInfo_danjuan(number)


def getHistoryRecord(url):
    if len(url) != 38 and len(url) != 58:
        return None

    if len(url) == 38:
        number = url[30:38]
        return getHistoryRecord_qieman(number)
    elif len(url) == 58:
        number = url[32:39]
        return getHistoryRecord_danjuan(number)


def formatTime(second):
    second /= 1000
    time_array = time.localtime(second)
    format_date = time.strftime("%Y-%m-%d", time_array)
    return format_date

def getFundInfo_qieman(number):
    url = 'https://qieman.com/pmdj/v1/pomodels/'+number
    try:
        response = requests.get(url=url, headers=qm_header)
        response.raise_for_status()
        content = response.text

        obj = json.loads(content)

        # 编号
        # number = obj.get('poCode')
        # URL
        sourse_url = 'https://qieman.com/portfolios/' + number
        # 名字
        name = obj.get('poName')
        # 粉丝数量
        followers = obj.get('followCount')
        # 成立日
        found_date = obj.get('establishedOn')
        # 年化收益率
        rate_per_ann = obj.get('annualCompoundedReturn')
        # 累计收益
        income_since_found = obj.get('fromSetupReturn')
        # 最大回撤
        max_drawdown = obj.get('maxDrawdown')
        # 年化波动率
        volatility = obj.get('volatility')
        # 夏普比率
        sharpe = obj.get('sharpe')

        return fund.fund(number=number, name=name, url=sourse_url, found_date=found_date,
                         max_drawdown=max_drawdown, volatility=volatility, sharpe_rate=sharpe,
                         rate_per_ann=rate_per_ann, income_since_found=income_since_found, followers=followers)
    except requests.HTTPError as e:
        print(e)
        print('status_code:',response.status_code)
        return None
    except Exception as e:
        print(e)
        return None

def getHistoryRecord_qieman(number):
    url = "https://qieman.com/pmdj/v1/pomodels/"+number+"/nav-history"
    try:
        response = requests.get(url=url, headers=qm_header)
        response.raise_for_status()
        content = response.text
        items = json.loads(content)
        records = []
        for item in items:
            nav = item.get('nav')
            if item.get('dailyReturn') is not None:
                daily_rd = item.get('dailyReturn') * 100
            else:
                daily_rd = None
            date = formatTime(item.get('navDate'))
            records.append(record.record(number=number, net_assert_value=nav, daily_rise_drop=daily_rd, date=date))
        return records
    except requests.HTTPError as e:
        print(e)
        print('status_code:',response.status_code)
        return None
    except Exception as e:
        print(e)
        return None




def getFundInfo_danjuan(number):
    url = "http://danjuanapp.com/djapi/plan/"+number

    try:
        response = requests.get(url=url, headers=dj_header)
        response.raise_for_status()
        content = response.text

        obj = json.loads(content)
        obj = obj.get('data')

        # 编号
        # number = obj.get('plan_code')
        # URL
        sourse_url = 'https://danjuanapp.com/strategy/' + number + '?channel=1300100141'
        # 名字
        name = obj.get('plan_name')
        # 累计收益
        income_since_found = obj.get('yield')
        # 成立以来年化率
        rate_per_ann = obj.get('yield_middle')
        # 成立日
        found_date = obj.get('found_date')

        url = "https://danjuanapp.com/djapi/plan/nav/indicator?plan_code=" + number

        response = requests.get(url=url, headers=dj_header)
        content = response.text

        obj = json.loads(content)
        obj = obj.get('data')

        # 最大回撤
        max_drawdown = obj.get('max_drawdown')
        # 年化波动率
        volatility = obj.get('volatility')
        # 夏普比率
        sharpe = obj.get('sharpe')

        return fund.fund(number=number, name=name, url=sourse_url, found_date=found_date,
                         max_drawdown=max_drawdown, volatility=volatility, sharpe_rate=sharpe,
                         rate_per_ann=rate_per_ann, income_since_found=income_since_found)
    except requests.HTTPError as e:
        print(e)
        print('status_code:',response.status_code)
        return None
    except Exception as e:
        print(e)
        return None




def getHistoryRecord_danjuan(number):
    url = "https://danjuanapp.com/djapi/plan/nav/history/"+number+"?size=30000&page=1"

    try:
        response = requests.get(url=url, headers=dj_header)
        response.raise_for_status()
        content = response.text

        obj = json.loads(content)
        obj = obj.get('data')
        items = obj.get('items')

        records = []

        for item in items:
            nav = item.get('nav')
            daily_rd = item.get('percentage')
            date = item.get('date')
            records.append(record.record(number=number, net_assert_value=nav, daily_rise_drop=daily_rd, date=date))

        return records
    except requests.HTTPError as e:
        print(e)
        print('status_code:',response.status_code)
        return None
    except Exception as e:
        print(e)
        return None




if __name__ == '__main__':
    danjuan = ['https://danjuanapp.com/strategy/CSI1033?channel=1300100141',
               'https://danjuanapp.com/strategy/CSI1032?channel=1300100141',
               'https://danjuanapp.com/strategy/CSI1038?channel=1300100141',
               'https://danjuanapp.com/strategy/CSI1029?channel=1300100141',
               'https://danjuanapp.com/strategy/CSI1006?channel=1300100141',
               'https://danjuanapp.com/strategy/CSI1065?channel=1300100141']

    qieman = ['https://qieman.com/portfolios/ZH010246',
              'https://qieman.com/portfolios/ZH006498',
              'https://qieman.com/portfolios/ZH000193',
              'https://qieman.com/portfolios/ZH001798',
              'https://qieman.com/portfolios/ZH012926',
              'https://qieman.com/portfolios/ZH009664',
              'https://qieman.com/portfolios/ZH030684',
              'https://qieman.com/portfolios/ZH017252',
              'https://qieman.com/portfolios/ZH035411',
              'https://qieman.com/portfolios/ZH043108']







# 2022/5/28
# 1653721631613
# 1653721631605
# 1653727893093
# 1653730656663 7D079C8A719AD10D16316A36483A31E3
# 2022/5/29
# 1653795439623 C12B49A01D606EF1052A1F019DD11286
# 1653795567864 E58836E5F71CC894F3A63372CA6A5D2D
# 2022/5/30
# 1653899940737 72A072AC9C8DB93EBE4AC030E83FFA64
# 2022/6/1
# 1654098370411 91E9B60F728EB9BC3AAF27330D0BE38D
# 2022/6/2
# 1654134810875 4C1CA98C7E0D820B2D5F8CC1BAC7CFB7
# 2022/6/3
# 1654245014670 09D30CFCCDB475FA9F196B651A85A6CE