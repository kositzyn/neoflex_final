from datetime import datetime, timedelta

import os

import pandas as pd
import numpy as np
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import booking


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


def booking_date_year(day, month, year, number):
    date = booking_date(day, month, year, number)
    return datetime.strftime(date, '%Y')


async def dataframe_to_sql(df: pd.DataFrame, session: AsyncSession = None):
    new_df = pd.DataFrame()

    new_df['booking_date'] = np.vectorize(booking_date)(df['arrival_date_day_of_month'],
                                                        df['arrival_date_month'],
                                                        df['arrival_date_year'],
                                                        df['lead_time'])
    new_df['length_of_stay'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']
    new_df['guest_name'] = df['name']
    new_df['daily_rate'] = df['adr']

    result = new_df.to_dict()

    for i in range(len(new_df)):
        stmt = insert(booking).values(booking_date=result['booking_date'][i],
                                      length_of_stay=result['length_of_stay'][i],
                                      guest_name=result['guest_name'][i] + 'checking',
                                      daily_rate=result['daily_rate'][i])
        await session.execute(stmt)
        await session.commit()
