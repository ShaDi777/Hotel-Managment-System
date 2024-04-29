CREATE TABLE IF NOT EXISTS payments (
    payment_id BIGSERIAL PRIMARY KEY,
    reservation_id BIGINT REFERENCES reservations(reservation_id),
    check_sum NUMERIC(10, 2),
    payment_date TIMESTAMP
);