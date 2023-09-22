from fastapi import APIRouter, Depends

from app.booking.utils import get_dataframe
from app.booking.utils import date_from_columns
from app.booking.utils import booking_date_month

from app.user.config import fastapi_users
from app.user.models import User


import pandas as pd
import numpy as np

current_user = fastapi_users.current_user()

bookings_routes = APIRouter(
    prefix='/bookings',
    tags=['Analysis for bookings']
)


@bookings_routes.get('/')
def get_all():
    pass


@bookings_routes.get('/nationality')
def get_by_nationality():
    pass


# Retrieves the most popular meal package among all bookings.
# Returns: The most popular meal package.
@bookings_routes.get('/get_popular_meal_package')
def get_popular_meal_package(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = df['meal'].value_counts().head(1)

    return result.to_dict()


@bookings_routes.get('/get_avg_length_of_stay')
def get_avg_length_of_stay():
    pass


# 9. Retrieves the total revenue grouped by booking month and hotel type.
# Returns: The total revenue for each combination of booking month and hotel type.
@bookings_routes.get('/total_revenue')
def get_total_revenue(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    df['booking_month'] = np.vectorize(booking_date_month)(df['arrival_date_day_of_month'],
                                                           df['arrival_date_month'],
                                                           df['arrival_date_year'],
                                                           df['lead_time'])

    df['total_stay'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']
    df['total_revenue'] = df['adr'] * df['total_stay']

    result = df.groupby(['hotel', 'booking_month'])['total_revenue'].sum().round(2)

    result_dict = dict()

    for i, row in result.items():
        i = tuple(i)
        if i[0] in result_dict:
            result_dict[i[0]].update({i[1]: row})
        else:
            result_dict[i[0]] = {i[1]: row}

    return result_dict


# 10. Retrieves the top 5 countries with the highest number of bookings.
# Returns: The top 5 countries with the most bookings.
@bookings_routes.get('/top_countries')
def get_top_countries(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = df['country'].value_counts().head(5)

    return {"data": result.to_dict()}


# 11. Retrieves the percentage of repeated guests among all bookings.
# Returns: The percentage of repeated guests.
@bookings_routes.get('/repeated_guests_percentage')
def get_repeated_guests_percentage(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = (len(df[df['is_repeated_guest'] == 1]) / len(df)) * 100

    return {"result": f'{result:.4f}'}


# 12. Retrieves the total number of guests (adults, children, and babies) by booking year.
# Returns: The total number of guests by booking year.
@bookings_routes.get('/total_guests_by_year')
def get_total_guests_by_year(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    df['sum'] = df[['adults', 'children', 'babies']].sum(axis=1)

    result = df[['sum', 'arrival_date_year']].groupby(['arrival_date_year']).sum()

    return result.to_dict()['sum']


# 13. Retrieves the average daily rate by month for resort hotel bookings.
# Returns: The average daily rate by month for resort hotel bookings.
@bookings_routes.get('/avg_daily_rate_resort')
def get_avg_daily_rate_resort(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = df[df['hotel'] == "Resort Hotel"].groupby(['arrival_date_month'])['adr'].mean().sort_values(
        ascending=False).round(2)

    return result.to_dict()


# 14. Retrieves the most common arrival date day of the week for city hotel bookings.
# Returns: The most common arrival date day of the week for city hotel bookings.
@bookings_routes.get('/most_common_arrival_day_city')
def get_most_common_arrival_day_city(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    d = {"January": '-01-', "February": '-02-', "March": '-03-', "April": '-04-',
         "May": '-05-', "June": '-06-', "July": '-07-', "August": '-08-',
         "September": '-09-', "October": '-10-', "November": '-11-', "December": '-12-'}

    new_df = df[df['hotel'] == "City Hotel"][['arrival_date_year',
                                              'arrival_date_month',
                                              'arrival_date_day_of_month']]
    new_df['date'] = new_df['arrival_date_year'].astype(str) + new_df['arrival_date_month'].astype(str).apply(
        lambda x: d[x]) + new_df['arrival_date_day_of_month'].apply(lambda x: str(x).rjust(2, '0'))
    new_df['date'] = pd.to_datetime(new_df['date']).dt.day_name()

    result = new_df['date'].value_counts().head(1)

    return result.to_dict()


# 15. Retrieves the count of bookings grouped by hotel type and meal package.
# Returns: The count of bookings by hotel type and meal package.
@bookings_routes.get('/count_by_hotel_meal')
def get_count_by_hotel_meal(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = df.groupby(['hotel', 'meal'])['adr'].count()

    result_dict = dict()

    for i, row in result.items():
        i = tuple(i)
        if i[0] in result_dict:
            result_dict[i[0]].update({i[1]: row})
        else:
            result_dict[i[0]] = {i[1]: row}

    return result_dict


# 16. Retrieves the total revenue by country for resort hotel bookings.
# Returns: The total revenue by country for resort hotel bookings.
@bookings_routes.get('/total_revenue_resort_by_country')
def get_total_revenue_resort_by_country(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    df['total_stay'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']
    df['total_revenue'] = df['adr'] * df['total_stay']
    result = df[df['hotel'] == "Resort Hotel"].groupby(['country'])['total_revenue'].sum()

    return result.to_dict()


# 17. Retrieves the count of bookings grouped by hotel type and repeated guest status.
# Returns: The count of bookings by hotel type and repeated guest status.
@bookings_routes.get('/count_by_hotel_repeated_guest')
def get_count_by_hotel_repeated_guest(_user: User = Depends(current_user)):
    df = get_dataframe(_user.csvfile)

    result = df.groupby(['hotel', 'is_repeated_guest'])['adr'].count()

    result_dict = dict()

    for i, row in result.items():
        i = tuple(i)
        if i[0] in result_dict:
            result_dict[i[0]].update({i[1]: row})
        else:
            result_dict[i[0]] = {i[1]: row}

    return result_dict


@bookings_routes.get('/search')
def get_search():
    pass


@bookings_routes.get('/stats')
def get_stats():
    pass


@bookings_routes.get('/analysis')
def get_analysis():
    pass


@bookings_routes.get('/{booking_id}')
def get_count_by_hotel_repeated_guest(booking_id: int):
    pass
