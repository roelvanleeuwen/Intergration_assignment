import datetime
import pandas as pd


def supply(start: int = 50, period: int = 7):
    dateparse = lambda x: datetime.datetime.strptime(x, '%d-%m-%Y %H:%M')
    production = pd.read_csv('Sheet1.csv', delimiter=';', encoding='utf-8', parse_dates=['Time (UTC)'],
                             date_parser=dateparse)
    stop = start + period

    period_production = (production.iloc[start * 24: stop * 24])
    return period_production

def supply2(start: int = 50, period: int = 7):
    dateparse = lambda x: datetime.datetime.strptime(x, '%d-%m-%Y %H:%M')
    production = pd.read_csv('Sheet1.csv', delimiter=';', encoding='utf-8', parse_dates=['Time (UTC)'],
                             date_parser=dateparse)
    stop = start + period

    period_production = (production.iloc[start * 24: stop * 24])
    return period_production