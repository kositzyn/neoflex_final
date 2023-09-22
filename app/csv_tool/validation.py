import os

# Sorted list of columns name
index = ['adr', 'adults', 'agent', 'arrival_date_day_of_month', 'arrival_date_month', 'arrival_date_week_number',
         'arrival_date_year', 'assigned_room_type', 'babies', 'booking_changes', 'children', 'company', 'country',
         'credit_card', 'customer_type', 'days_in_waiting_list', 'deposit_type', 'distribution_channel', 'email',
         'hotel', 'is_canceled', 'is_repeated_guest', 'lead_time', 'market_segment', 'meal', 'name', 'phone-number',
         'previous_bookings_not_canceled', 'previous_cancellations', 'required_car_parking_spaces',
         'reservation_status', 'reservation_status_date', 'reserved_room_type', 'stays_in_week_nights',
         'stays_in_weekend_nights', 'total_of_special_requests']


def is_csv_valid(line) -> bool:
    line = line.decode('utf-8')
    lst = line.split(',')
    lst = [element.strip() for element in lst]
    if sorted(lst) == index:
        return True
    return False


def create_temporary() -> None:
    """
    Check existing of /temporary. If not, create it
    and add .gitignore file for this directory

    /temporary is directory for uploaded files
    """
    if not os.path.exists('temporary'):
        os.mkdir('temporary')
        with open('temporary/.gitignore', 'w+') as git_ignore_file:
            git_ignore_file.writelines('*')
