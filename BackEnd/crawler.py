import requests
import json
import time

qm_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'x-sign': '1653795439623C12B49A01D606EF1052A1F019DD11286'
}

dj_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

def formatTime(second):
    time_array = time.localtime(second)
    format_date = time.strftime("%Y-%m-%d", time_array)
    print(format_date)

def getFundInfo_qieman(number):
    url = 'https://qieman.com/pmdj/v1/pomodels/'+number
    response = requests.get(url=url, headers=qm_header)
    content = response.text
    obj = json.loads(content)
    # 编号
    number = obj.get('poCode')
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

def getHistoryRecord_qieman(number):
    url = "https://qieman.com/pmdj/v1/pomodels/"+number+"/nav-history"
    response = requests.get(url=url, headers=qm_header)
    content = response.text
    obj = json.loads(content)

def getFundInfo_danjuan(number):
    url = "http://danjuanapp.com/djapi/plan/"+number

    response = requests.get(url=url, headers=dj_header)
    content = response.text

    obj = json.loads(content)
    obj = obj.get('data')

    # 编号
    number = obj.get('plan_code')
    # 名字
    name = obj.get('plan_name')
    # 累计收益
    income_since_found = obj.get('yield')
    # 成立以来年化率
    rate_per_ann = obj.get('yield_middle')
    # 成立日
    found_date = obj.get('found_date')

    url = "https://danjuanapp.com/djapi/plan/nav/indicator?plan_code="+number

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

def getHistoryRecord_danjuan(number):
    url = "https://danjuanapp.com/djapi/plan/nav/history/"+number+"?size=5000&page=1"

    response = requests.get(url=url, headers=dj_header)
    content = response.text

    obj = json.loads(content)
    obj = obj.get('data')
    list = obj.get('items')

    records = []

    for item in list:
        nav = item.get('nav')
        daily_rd = item.get('percentage')







# 1653721631613
# 1653721631605
# 1653727893093
# 1653730656663 7D079C8A719AD10D16316A36483A31E3

# 1653795439623 C12B49A01D606EF1052A1F019DD11286
# 1653795567864 E58836E5F71CC894F3A63372CA6A5D2D