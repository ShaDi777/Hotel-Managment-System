# вывести все свободные комнаты на определенный период времени
from datetime import datetime, timedelta
import random


def get_random_dates():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    random_start_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    random_end_date = random_start_date + timedelta(days=random.randint(0, (end_date - random_start_date).days))
    return random_start_date, random_end_date


def get_free_rooms_query():
    start_date, end_date = get_random_dates()

    return f""" SELECT r.room_id
                FROM rooms r
                WHERE NOT EXISTS (
                SELECT 1
                    FROM reservations res
                    WHERE res.room_id = r.room_id
                    AND res.check_in_date < '{end_date}'::date
                    AND res.check_out_date > '{start_date}'::date
                ); """
