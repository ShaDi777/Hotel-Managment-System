import os
import sys
import time
from faker import Faker
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from datetime import datetime, timedelta
import random
import threading

# Создание экземпляра Faker для генерации данных
fake = Faker()

# Функция для генерации случайной даты в указанном диапазоне
def generate_random_date(start_date, end_date):
    return fake.date_time_between_dates(start_date=start_date, end_date=end_date)

# Функция для генерации случайного диапазона дат для спец. предложений
def generate_random_dates():
    start_date = fake.date_this_year()
    end_date = start_date + timedelta(days=random.randint(1, 30))
    return start_date, end_date

# Функция для выполнения SQL-запроса
def execute_query(query, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        # print(f"Could not execute {query}. Exception: {e}")

def get_records_count(table_name, conn):
    queryCount = sql.SQL(f"SELECT count(*) FROM {table_name}")
    cursor = conn.cursor()
    cursor.execute(queryCount)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.commit()
    return result

# Функция для генерации данных для таблицы rooms
def generate_rooms_data(conn, num_records):
    count = get_records_count("rooms", conn)
    
    for _ in range(count, num_records, 1):
        rooms_amount = fake.random_int(min=1, max=10)
        daily_price = fake.random_number(digits=4) + fake.random_number(digits=2) / 100
        query = sql.SQL("INSERT INTO rooms (rooms_amount, daily_price) VALUES ({}, {})").format(
            sql.Literal(rooms_amount), sql.Literal(daily_price)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы comforts
def generate_comforts_data(conn, num_records):
    count = get_records_count("comforts", conn)
    for _ in range(count, num_records, 1):
        comfort_name = fake.word()
        query = sql.SQL("INSERT INTO comforts (comfort_name) VALUES ({})").format(sql.Literal(comfort_name))
        execute_query(query, conn)

# Функция для генерации данных для таблицы rooms_comforts
def generate_rooms_comforts_data(conn, num_records, rooms_count, comforts_count):
    count = get_records_count("rooms_comforts", conn)
    for _ in range(count, num_records, 1):
        room_id = random.randint(1, rooms_count)
        comfort_id = random.randint(1, comforts_count)
        amount = fake.random_int(min=1, max=5)
        query = sql.SQL("INSERT INTO rooms_comforts (room_id, comfort_id, amount) VALUES ({}, {}, {})").format(
            sql.Literal(room_id), sql.Literal(comfort_id), sql.Literal(amount)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы special_offers
def generate_special_offers_data(conn, num_records, rooms_count):
    count = get_records_count("special_offers", conn)
        
    for _ in range(count, num_records, 1):
        room_id = random.randint(1, rooms_count)
        discount_percent = fake.random_number(digits=2) + fake.random_number(digits=2) / 100
        start_date, end_date = generate_random_dates()
        query = sql.SQL("INSERT INTO special_offers (room_id, discount_percent, start_date, end_date) VALUES ({}, {}, {}, {})").format(
            sql.Literal(room_id), sql.Literal(discount_percent), sql.Literal(start_date), sql.Literal(end_date)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы guests
def generate_guests_data(conn, num_records):
    count = get_records_count("guests", conn)
        
    for _ in range(count, num_records, 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.address()
        query = sql.SQL("INSERT INTO guests (first_name, last_name, email, phone_number, address) VALUES ({}, {}, {}, {}, {})").format(
            sql.Literal(first_name), sql.Literal(last_name), sql.Literal(email), sql.Literal(phone_number), sql.Literal(address)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы reservations
def generate_reservations_data(conn, num_records, rooms_count):
    count = get_records_count("reservations", conn)
        
    for _ in range(count, num_records, 1):
        room_id = random.randint(1, rooms_count)
        check_in_date = fake.date_this_year()
        check_out_date = check_in_date + timedelta(days=random.randint(1, 30))
        query = sql.SQL("INSERT INTO reservations (room_id, check_in_date, check_out_date) VALUES ({}, {}, {})").format(
            sql.Literal(room_id), sql.Literal(check_in_date), sql.Literal(check_out_date)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы reservations_guests
def generate_reservations_guests_data(conn, num_records, reservations_count, guests_count):
    count = get_records_count("reservations_guests", conn)
        
    for _ in range(count, num_records, 1):
        reservation_id = random.randint(1, reservations_count)
        guest_id = random.randint(1, guests_count)
        query = sql.SQL("INSERT INTO reservations_guests (reservation_id, guest_id) VALUES ({}, {})").format(
            sql.Literal(reservation_id), sql.Literal(guest_id)
        )
        execute_query(query, conn)

def generate_reviews_data(conn, num_reviews):
    count = get_records_count("reviews", conn)

    batch_size = 1000  # Размер порции записей для обработки
    start_batch = (count // batch_size) + 1
    num_batches = num_reviews // batch_size
    remaining_reviews = num_reviews % batch_size
    
    for i in range(start_batch, num_batches, 1):
        offset = i * batch_size  # Вычисляем смещение для текущего пакета
        generate_reviews_batch(conn, batch_size, offset)
    
    # Обрабатываем оставшиеся отзывы (если есть)
    if start_batch < num_batches and remaining_reviews > 0:
        offset = num_batches * batch_size
        generate_reviews_batch(conn, remaining_reviews, offset)

def generate_reviews_batch(conn, batch_size, offset):
    # Получаем записи из таблицы reservations_guests с использованием LIMIT и OFFSET
    query = "SELECT reservation_id, guest_id FROM reservations_guests ORDER BY reservation_id, guest_id LIMIT %s OFFSET %s;"
    cursor = conn.cursor()
    cursor.execute(query, (batch_size, offset))
    records = cursor.fetchall()
    cursor.close()
    
    # Генерируем отзывы для каждой выбранной записи
    for record in records:
        reservation_id, guest_id = record
        rating = round(random.uniform(1, 5), 2)
        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        review_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        insert_query = sql.SQL("INSERT INTO reviews (reservation_id, guest_id, rating, comment, review_date) VALUES ({}, {}, {}, {}, {})").format(
            sql.Literal(reservation_id), sql.Literal(guest_id), sql.Literal(rating), sql.Literal(comment), sql.Literal(review_date)
        )
        execute_query(insert_query, conn)

# Функция для генерации данных для таблицы payments
def generate_payments_data(conn, num_records, reservations_count):
    count = get_records_count("payments", conn)
        
    for _ in range(count, num_records, 1):
        reservation_id = random.randint(1, reservations_count)
        check_sum = fake.random_number(digits=4) + fake.random_number(digits=2) / 100
        payment_date = fake.date_this_month()
        query = sql.SQL("INSERT INTO payments (reservation_id, check_sum, payment_date) VALUES ({}, {}, {})").format(
            sql.Literal(reservation_id), sql.Literal(check_sum), sql.Literal(payment_date)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы employees
def generate_employees_data(conn, num_records):
    count = get_records_count("employees", conn)
        
    for _ in range(count, num_records, 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        query = sql.SQL("INSERT INTO employees (first_name, last_name) VALUES ({}, {})").format(
            sql.Literal(first_name), sql.Literal(last_name)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы departments
def generate_departments_data(conn, num_records):
    count = get_records_count("departments", conn)
        
    for _ in range(count, num_records, 1):
        department_name = fake.word()
        query = sql.SQL("INSERT INTO departments (department_name) VALUES ({})").format(
            sql.Literal(department_name)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы positions
def generate_positions_data(conn, num_records):
    count = get_records_count("positions", conn)
        
    for _ in range(count, num_records, 1):
        position_name = fake.word()
        query = sql.SQL("INSERT INTO positions (position_name) VALUES ({})").format(
            sql.Literal(position_name)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы employees_departments
def generate_employees_departments_data(conn, num_records, employees_count, departments_count):
    count = get_records_count("employees_departments", conn)
        
    for _ in range(count, num_records, 1):
        employee_id = random.randint(1, employees_count)
        department_id = random.randint(1, departments_count)
        query = sql.SQL("INSERT INTO employees_departments (employee_id, department_id) VALUES ({}, {})").format(
            sql.Literal(employee_id), sql.Literal(department_id)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы employees_positions
def generate_employees_positions_data(conn, num_records, employees_count, positions_count):
    count = get_records_count("employees_positions", conn)
        
    for _ in range(count, num_records, 1):
        employee_id = random.randint(1, employees_count)
        position_id = random.randint(1, positions_count)
        query = sql.SQL("INSERT INTO employees_positions (employee_id, position_id) VALUES ({}, {})").format(
            sql.Literal(employee_id), sql.Literal(position_id)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы services
def generate_services_data(conn, num_records):
    count = get_records_count("services", conn)
        
    for _ in range(count, num_records, 1):
        service_name = fake.word()
        description = fake.text()
        query = sql.SQL("INSERT INTO services (service_name, description) VALUES ({}, {})").format(
            sql.Literal(service_name), sql.Literal(description)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы provided_services
def generate_provided_services_data(conn, num_records, services_count, employees_count):
    count = get_records_count("provided_services", conn)
        
    for _ in range(count, num_records, 1):
        service_id = random.randint(1, services_count)
        employee_id = random.randint(1, employees_count)
        price = fake.random_number(digits=4) + fake.random_number(digits=2) / 100
        query = sql.SQL("INSERT INTO provided_services (service_id, employee_id, price) VALUES ({}, {}, {})").format(
            sql.Literal(service_id), sql.Literal(employee_id), sql.Literal(price)
        )
        execute_query(query, conn)

# Функция для генерации данных для таблицы reservations_provided_services
def generate_reservations_provided_services_data(conn, num_records, provided_services_count, reservations_count):
    count = get_records_count("reservations_provided_services", conn)
        
    for _ in range(count, num_records, 1):
        provided_service_id = random.randint(1, provided_services_count)
        reservation_id = random.randint(1, reservations_count)
        request_date = fake.date_this_year()
        query = sql.SQL("INSERT INTO reservations_provided_services (provided_service_id, reservation_id, request_date) VALUES ({}, {}, {})").format(
            sql.Literal(provided_service_id), sql.Literal(reservation_id), sql.Literal(request_date)
        )
        execute_query(query, conn)

def create_conn():
    exception = None
    retries = 0
    max_retries = 100
    conn = None
    while retries < max_retries:
        try:
            # Установка параметров подключения к базе данных
            conn = psycopg2.connect(
                dbname="hotel",
                user="postgres",
                password="postgres",
                host="db"
            )
            print("Database connection successful")
            break
        except OperationalError as e:
            exception = e
            retries += 1
            print(e)
            time.sleep(5)

    if conn is not None:
        return conn
    else:
        raise exception

def generate_data(num_records):
    # Устанавливаем соединение с базой данных
    conn = create_conn()

    # Получаем количество комнат, удобств и сотрудников
    rooms_count = num_records
    comforts_count = num_records
    employees_count = num_records
    departments_count = num_records
    positions_count = num_records
    services_count = num_records
    provided_services_count = num_records
    reservations_count = num_records
    guests_count = num_records

    # Генерируем данные для каждой таблицы
    generate_rooms_data(conn, num_records)
    generate_comforts_data(conn, num_records)
    generate_rooms_comforts_data(conn, num_records, rooms_count, comforts_count)
    generate_special_offers_data(conn, num_records, rooms_count)
    generate_guests_data(conn, num_records)
    generate_reservations_data(conn, num_records, rooms_count)
    generate_reservations_guests_data(conn, num_records, reservations_count, guests_count)
    generate_reviews_data(conn, num_records)
    generate_payments_data(conn, num_records, reservations_count)
    generate_employees_data(conn, num_records)
    generate_departments_data(conn, num_records)
    generate_positions_data(conn, num_records)
    generate_employees_departments_data(conn, num_records, employees_count, departments_count)
    generate_employees_positions_data(conn, num_records, employees_count, positions_count)
    generate_services_data(conn, num_records)
    generate_provided_services_data(conn, num_records, services_count, employees_count)
    generate_reservations_provided_services_data(conn, num_records, provided_services_count, reservations_count)

    # Закрываем соединение с базой данных
    conn.close()

if __name__ == "__main__":
    num_records = int(os.getenv('NUM_RECORDS', 1_000_000))
    print(f"Total records: {num_records}")
    generate_data(num_records)
