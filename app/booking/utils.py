from datetime import datetime, timedelta

import os

import pandas as pd


def get_dataframe(filename: str):
    if os.path.isfile("temporary/" + filename):
        return pd.read_csv("temporary/" + filename)
    else:
        return pd.read_csv("demo/hotel_booking_data.csv")


def date_from_columns(day, month, year):
    date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%B-%d')
    return date


def booking_date(day, month, year, number):
    return date_from_columns(day, month, year) - timedelta(days=int(number))


def booking_date_month(day, month, year, number):
    date = booking_date(day, month, year, number)
    return datetime.strftime(date, '%B')