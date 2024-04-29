# вывести историю всех аренд для одного пользователя

def get_random_guest_id(conn):
    query = f"""
            SELECT guest_id
            FROM guests
            OFFSET random() * (SELECT COUNT(*) FROM guests)
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


def get_guest_history_query(conn):
    return f""" SELECT * FROM reservations_guests rg
                JOIN reservations r
                ON rg.reservation_id = r.reservation_id
                WHERE rg.guest_id = {get_random_guest_id(conn)}; """

