import xlwt

import utils
import time
from joblib import dump, load
import yfinance as yf


def automation():
    """
    Automating the process. Once every minute the function checks if there are new news from SeekingAlpha.com. If there
    are it will check with the ML model and decide if it should purchase the stock or not.
    Automatically it will sell the stock at 9:30 am of the next day (the stock-market opening time).

    :return:
    """
    book = xlwt.Workbook(encoding="utf-8")
    purchased = list()
    purchase_at_opening = []
    sheet = book.add_sheet("Sheet 1")
    model = load('model_final.joblib')
    counter = 0
    while True:
        news = utils.get_latest()
        print(news)
        if news == "not a stock news":
            time.sleep(60)
            continue

        symbol = news[0]
        text = news[1]
        prediction = model.predict(utils.simple(text))

        time_ = news[2].split(" ")[3]
        time_sign = news[2].split(" ")[4]
        hour = int(time_.split(':')[0]) + int(time_.split(':')[1]) / 60

        # fix data to 24 system from 12 system
        if time_sign == 'PM' and not round(hour - 0.49) == 12:
            hour += 12
        if hour < 9.5 or (time_.split(':')[0] == '12' and time_sign == 'AM'):
            purchase_at_opening.append(symbol)
        elif hour > 16:
            print("after work hours")

        if date() - sell() < 300:
            sell_all(purchased)
            purchase_all(purchase_at_opening, purchased, counter, sheet)
        if prediction:
            counter += 1
            buy(symbol, sheet, counter, purchased)
        time.sleep(60)
        book.save("book")


def buy(symbol, sheet, counter, purchased):
    """
    Buys the stock

    :param symbol: stock symbol to purchase
    :param sheet: sheet for the data
    :param counter: counter for the data in the sheet
    :param purchased: list of purchased stocks
    :return: purchased stock price
    """
    stock = yf.Ticker(symbol)
    price = stock.history()["Close"][-1]
    # sheet.write(counter, 1, "Purchase")
    # sheet.write(counter, 2, symbol)
    cur_date = date()
    # sheet.write(counter, 3, cur_date)
    # sheet.write(counter, 4, price)
    print("Purchase", symbol, cur_date, price)
    purchased.append((symbol, cur_date))
    # implement stock purchasing
    return price


def purchase_all(lst, purchased, counter, sheet):
    """
    Purchases all the stocks in a list

    :param lst: list of stocks symbols to purchase
    :param purchased: list of purchased stocks
    :param counter: sheet for the data
    :param sheet: counter for the data in the sheet
    :return: None
    """
    for i in lst:
        buy(i, sheet, counter, purchased)
        counter += 1


def sell_all(purchased):
    """
    Sells all stocks from the list

    :param purchased: list of purchased stock to sell
    :return: None
    """
    for i in purchased:
        if (date() - i[1]).total_seconds() > 60000:
            sell(i[0])
            purchased.pop(i)


def sell(symbol, sheet, counter):
    """
    Sells the stock

    :param symbol: stock symbol
    :param sheet: sheet for the data
    :param counter: counter for the data in the sheet
    :return: sold stock price
    """
    stock = yf.Ticker(symbol)
    price = stock.history()["Close"][-1]
    # sheet.write(counter, 1, "Sell")
    # sheet.write(counter, 2, symbol)
    # sheet.write(counter, 3, date())
    # sheet.write(counter, 4, price)
    print("Sell", symbol, date(), price)
    return price


def date():
    """
    Generates current time EST

    :return: current time EST
    """
    from datetime import datetime
    from pytz import timezone
    # define date format
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # define eastern timezone
    eastern = timezone('US/Eastern')
    # localized datetime
    loc_dt = datetime.now(eastern)
    time_ = datetime(loc_dt.year, loc_dt.month, loc_dt.day, loc_dt.hour, loc_dt.minute, loc_dt.second, 00)
    return time_


def sell_date():
    """
    Generates datetime of current day at 9:30 am

    :return: sell time
    """
    from datetime import datetime
    from pytz import timezone
    # define date format
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # define eastern timezone
    eastern = timezone('US/Eastern')
    # localized datetime
    loc_dt = datetime.now(eastern)
    sell_time_ = datetime(loc_dt.year, loc_dt.month, loc_dt.day, 9, 30, 00, 00)
    return sell_time_


if __name__ == "__main__":
    automation()
