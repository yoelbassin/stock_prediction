import math
import yfinance as yf
import utils
import xlwt


def get_data(i, num=0):
    """
    Creates a list of (num) clean HTML news from page (i)  (Stock symbol, news text and data)

    :param i: page number
    :param num: number of wanted news from page (i)
    :return: list of (Stock symbol, news text and data)
    """
    containers = utils.get_news(i)
    news_list = list()
    for i in range(num + 1):
        s = utils.get_text(containers[i])
        if s == "not a stock news":
            continue
        news_list.append(s)
    return news_list


def create_training_set(start_page, finish_page, book_name):
    """
    Creates the training set into Excel book from SeekingAlpha.com news pages

    :param start_page: SeekingAlpha.com start page fot the training set
    :param finish_page: SeekingAlpha.com end page fot the training set
    :param book_name: Book name for the training data
    :return: None
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1 Today's Close")
    sheet2 = book.add_sheet("Sheet 2 Tomorrow's Start")
    sheet3 = book.add_sheet("Sheet 3 24 hours later")
    sheet4 = book.add_sheet("Sheet 4 Tomorrow's Close")

    counter1, counter2 = 0, 0

    def add(sheet, start_date, time_, time_sign, end_date, end_time, end_time_sign, start_price, end_price, news,
            counter):
        """
        Adds stock data to Excel book sheet

        :param sheet: selected sheet
        :param start_date: purchase date
        :param time_: purchase time
        :param time_sign: AM / PM
        :param end_date: sell date
        :param end_time: sell time
        :param end_time_sign: AM / PM
        :param start_price: purchase price
        :param end_price: sell price
        :param news: Stock symbol, news text and date
        :param counter: news number counter
        :return: None
        """
        change = 100 * (end_price - start_price) / start_price
        print(change)
        if math.isnan(change):
            print("Nan")
            return
        # symbol
        sheet.write(counter, 0, news[0])
        # news
        sheet.write(counter, 1, news[1])
        # y value
        if change >= 0:
            sheet.write(counter, 2, 1)
        else:
            sheet.write(counter, 2, 0)
        # start date and time
        sheet.write(counter, 3, start_date + " " + time_ + " " + time_sign)
        # end date and time
        sheet.write(counter, 4, end_date + " " + end_time + " " + end_time_sign)
        # purchase price
        sheet.write(counter, 5, start_price)
        # sell price
        sheet.write(counter, 6, end_price)
        # stock price change
        sheet.write(counter, 7, end_price - start_price)
        # percentage change
        sheet.write(counter, 8, str(change) + '%')

    def get_stock_data(news, count1, count2):
        """
        Generates stock data

        :param news: Stock symbol, news text and data
        :param count1: counter 1
        :param count2: counter 2
        :return: None
        """
        try:
            months = ['blank', "Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.",
                      "Dec."]
            days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            # Generate time data
            print(news)
            month = news[2].split(" ")[1]
            day = int(news[2].split(" ")[2][:-1])
            time_ = news[2].split(" ")[3]
            time_sign = news[2].split(" ")[4]
            hour = int(time_.split(':')[0]) + int(time_.split(':')[1]) / 60

            # fix data to 24 system from 12 system
            if time_sign == 'PM' and not round(hour - 0.49) == 12:
                hour += 12
            if hour < 9.5 or (time_.split(':')[0] == '12' and time_sign == 'AM'):
                hour = 9.5
            elif hour > 16:
                print("after work hours")
                return count1, count2
            # news and purchase date
            org_date = "2020-" + str(months.index(month)) + '-' + str(day)
            time_block = round((hour - 9.5) * 4)

            # Next day
            if day + 1 > days[months.index(month)]:
                month = months[months.index(month) + 1]
                day = 0
            sec_day = "2020-" + str(months.index(month)) + '-' + str(day + 1)

            # Two days later
            if day + 2 > days[months.index(month)]:
                month = months[months.index(month) + 1]
                day = -1
            third_day = "2020-" + str(months.index(month)) + '-' + str(day + 2)

            print(org_date, hour)
            print(sec_day, third_day)

            # get purchase day info
            try:
                hist = yf.Ticker(news[0]).history(start=org_date, end=sec_day, interval='15m')["Close"]
                start_price = hist[time_block]
                if math.isnan(start_price):
                    start_price = hist[1]
                # sheet 1
                close_today_price = hist[-1]
                add(sheet1, org_date, time_, time_sign, org_date, "4:00", "PM", start_price, close_today_price, news,
                    count1)
                count1 += 1
            except:
                print("No start data")
                return count1, count2

            # get next day info
            try:
                hist = yf.Ticker(news[0]).history(start=sec_day, end=third_day, interval='15m')["Close"]
                # sheet 2
                start_next_day_price = hist[0]
                if math.isnan(start_next_day_price):
                    start_next_day_price = hist[1]
                print("start_next_day_price: ", end='')
                add(sheet2, org_date, time_, time_sign, sec_day, "9:30", "AM", start_price, start_next_day_price, news,
                    count2)
                # sheet 3
                while True:
                    try:
                        close_24_later_price = hist[time_block]
                        if math.isnan(close_24_later_price):
                            print("nan ", end='')
                            close_24_later_price = hist[time_block + 1]
                        break
                    except:
                        time_block -= 1
                print("close_24_later_price: ", end='')
                add(sheet3, org_date, time_, time_sign, sec_day, time_, time_sign, start_price, close_24_later_price,
                    news, count2)
                # sheet 4
                close_next_day_price = hist[-1]
                print("close_next_day_price: ", end='')
                add(sheet4, org_date, time_, time_sign, sec_day, "4:00", "PM", start_price, close_next_day_price, news,
                    count2)
                count2 += 1
                return count1, count2
            except:
                print("No next day data")
                return count1, count2

        except:
            print("No data found")
            return count1, count2

    # create training set
    for i in range(start_page, finish_page):
        print("page number: ", i)
        print(100 * ((i - start_page) / (finish_page - start_page)), "% done")
        p = get_data(i, 200)
        print(p)
        for j in p:
            counter1, counter2 = get_stock_data(j, counter1, counter2)

    book.save(book_name)


if __name__ == "__main__":
    create_training_set(6, 77)
