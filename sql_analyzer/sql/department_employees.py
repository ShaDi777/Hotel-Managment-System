# вывести всех сотрудников для определенного департамента

def get_random_department_id(conn):
    query = f"""
            SELECT department_id
            FROM departments
            OFFSET random() * (SELECT COUNT(*) FROM departments)
            LIMIT 1;
            """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result[0]
        else:
            return None
    except Exception as error:
        conn.rollback()
        print("Error:", error)
        return None


def get_department_employees_query(conn):
    return f""" SELECT * FROM employees_departments ed
                JOIN employees e
                ON ed.employee_id = e.employee_id
                WHERE ed.department_id = {get_random_department_id(conn)}; """
