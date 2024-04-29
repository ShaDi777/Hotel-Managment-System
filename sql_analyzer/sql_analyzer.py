# TODO change connection function 
import os
import json
import time
import psycopg2
import datetime

from sql.department_employees import get_department_employees_query
from sql.free_rooms import get_free_rooms_query
from sql.guest_history import get_guest_history_query
from sql.room_rating import get_room_ratings_query
from sql.rooms_with_comforts import get_rooms_with_comforts_query


now = datetime.datetime.now()


def create_conn():
    exception = None
    retries = 0
    max_retries = 100
    conn = None
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname="hotel",
                user="postgres",
                password="postgres",
                host="localhost"
                # host="db"
            )
            print("Database connection successful")
            break
        except psycopg2.OperationalError as e:
            exception = e
            retries += 1
            print(e)
            time.sleep(5)

    if conn is not None:
        return conn
    else:
        raise exception


def execute_query_and_analyze(conn, query_generator, num_attempts):
    cost = []
    planning = []
    execution = []

    query = ""
    cursor = conn.cursor()
    for attempt in range(num_attempts):
        query = query_generator()

        cursor.execute(f"EXPLAIN (FORMAT json, ANALYZE) {query}")
        explain_result = cursor.fetchone()[0][0]

        data = json.loads(json.dumps(explain_result))

        cost.append(float(data["Plan"]["Total Cost"]))
        planning.append(float(data["Planning Time"]))
        execution.append(float(data["Execution Time"]))
    cursor.close()

    save_performance(query, cost, planning, execution)


def generate_filename():
    result_directory = "results"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    formatted_datetime = now.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{result_directory}/performance_{formatted_datetime}.txt"
    return filename


def save_performance(query, cost, planning, execution):
    output_file = generate_filename()
    with open(output_file, 'a') as file:
        file.write("===================================\n")
        file.write(f"Query: {query}\n")
        file.write("===================================\n")

        file.write("COST:\n")
        file.write(f"\tBEST: {min(cost)}\n")
        file.write(f"\tAVERAGE: {sum(cost) / len(cost):.3f}\n")
        file.write(f"\tWORST: {max(cost)}\n")
        file.write("\n")

        file.write("PLANNING:\n")
        file.write(f"\tBEST: {min(planning)}\n")
        file.write(f"\tAVERAGE: {sum(planning) / len(planning):.3f}\n")
        file.write(f"\tWORST: {max(planning)}\n")
        file.write("\n")

        file.write("EXECUTION:\n")
        file.write(f"\tBEST: {min(execution)}\n")
        file.write(f"\tAVERAGE: {sum(execution) / len(execution):.3f}\n")
        file.write(f"\tWORST: {max(execution)}\n")
        file.write("===================================\n\n")


if __name__ == "__main__":
    conn = create_conn()
    num_attempts = int(os.environ.get('NUM_ATTEMPTS', 20))

    execute_query_and_analyze(conn, lambda: get_department_employees_query(conn), num_attempts)
    execute_query_and_analyze(conn, get_free_rooms_query, num_attempts)
    execute_query_and_analyze(conn, lambda: get_guest_history_query(conn), num_attempts)
    execute_query_and_analyze(conn, get_room_ratings_query, num_attempts)
    execute_query_and_analyze(conn, lambda: get_rooms_with_comforts_query(conn), num_attempts)
