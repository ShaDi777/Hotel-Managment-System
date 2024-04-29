CREATE TABLE IF NOT EXISTS reservations (
    reservation_id BIGSERIAL PRIMARY KEY,
    room_id BIGINT REFERENCES rooms(room_id),
    check_in_date TIMESTAMP,
    check_out_date TIMESTAMP
);