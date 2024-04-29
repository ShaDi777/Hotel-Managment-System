CREATE TABLE IF NOT EXISTS rooms (
    room_id BIGSERIAL PRIMARY KEY,
    rooms_amount INTEGER NOT NULL,
    daily_price NUMERIC(10, 2) NOT NULL
);