class fund:
    def __init__(self,number,name,url,found_date,max_drawdown,volatility,sharpe_rate,rate_per_ann,income_since_found,followers=None):
        self.number = number
        self.name = name
        self.url = url
        self.found_date = found_date
        self.max_drawdown = max_drawdown
        self.volatility = volatility
        self.sharpe_rate = sharpe_rate
        self.rate_per_ann = rate_per_ann
        self.income_since_found = income_since_found
        self.followers = followers
