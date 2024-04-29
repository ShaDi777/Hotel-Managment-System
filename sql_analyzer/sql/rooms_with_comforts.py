# все комнаты удовлетворяющие фильтрам комфорта
import random

def get_random_comfort_id(conn):
    query = f"""
            SELECT comfort_id
            FROM comforts
            OFFSET random() * (SELECT COUNT(*) FROM comforts)
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


def get_rooms_with_comforts_query(conn):
    return f""" SELECT DISTINCT rc.room_id
                FROM rooms_comforts rc
                WHERE rc.comfort_id = {get_random_comfort_id(conn)}
                AND rc.amount >= {random.randint(1, 10)}; """
