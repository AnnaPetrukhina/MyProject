from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import logging

from settings import FLIGHT_SCHEDULE


log = logging.getLogger('ChatBot')


def check_regular_date(flight_date, future_dates, date, date_end):
    if flight_date < date < date_end and len(future_dates) < 5:
        future_dates.append(date.strftime('%d-%m-%Y'))
    return future_dates


def regular_date(data, flight_date, ):
    future_dates = []
    re_month = r"\bмесяц"
    re_week = r"\bнедел"
    re_half_year = r"\bполгод"
    re_count = r"\b[1-9]"
    interval = data["interval"]["density"]
    date = datetime.strptime(data["interval"]["begin_time"], '%d-%m-%Y')
    end = datetime.strptime("16-12-3020", '%d-%m-%Y')
    date_end = datetime.strptime(data["interval"]["end_time"], '%d-%m-%Y') if data["interval"]["end_time"] else end
    count = int(re.search(re_count, interval)[0])
    if re.search(re_month, interval) is not None:
        for _ in range(5):
            future_dates = check_regular_date(flight_date=flight_date, future_dates=future_dates,
                                              date=date, date_end=date_end)
            date = date + relativedelta(months=count)
    elif re.search(re_half_year, interval) is not None:
        for _ in range(5):
            future_dates = check_regular_date(flight_date=flight_date, future_dates=future_dates,
                                              date=date, date_end=date_end)
            date = date + relativedelta(months=6)
    elif re.search(re_week, interval) is not None:
        for _ in range(5):
            future_dates = check_regular_date(flight_date=flight_date, future_dates=future_dates,
                                              date=date, date_end=date_end)
            date = date + relativedelta(weeks=count)
    else:
        log.info(f"не знаю что делать")
    return future_dates


def irregular_date(data, flight_date, ):
    future_dates = []
    dates = data["date"]
    dates.sort(key=lambda sort_date: datetime.strptime(sort_date, '%d-%m-%Y'))
    for date in dates:
        date = datetime.strptime(date, '%d-%m-%Y')
        if date >= flight_date and len(future_dates) < 5:
            future_dates.append(date.strftime('%d-%m-%Y'))
    return future_dates


def getting_date(flight_date, departure_city, arrival_city):
    data = FLIGHT_SCHEDULE[departure_city][arrival_city]
    flight_date = datetime.strptime(flight_date, '%d-%m-%Y')
    if data["date"] is None:
        future_dates = regular_date(data=data, flight_date=flight_date)
    else:
        future_dates = irregular_date(data=data, flight_date=flight_date)
    return [future_dates, data["name_of_flight"]]
