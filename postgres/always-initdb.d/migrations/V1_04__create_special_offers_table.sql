CREATE TABLE IF NOT EXISTS special_offers (
    offer_id BIGSERIAL PRIMARY KEY,
    room_id BIGINT REFERENCES rooms(room_id),
    discount_percent NUMERIC(6, 4) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);