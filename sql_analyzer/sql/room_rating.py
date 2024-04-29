# вывести комнаты и их сред рейтинг

def get_room_ratings_query() -> str:
    return f""" SELECT rms.room_id, AVG(rvw.rating)
                FROM reviews rvw
                JOIN reservations reserv
                ON rvw.reservation_id = reserv.reservation_id
                JOIN rooms rms
                ON reserv.room_id = rms.room_id
                GROUP BY rms.room_id; """
