CREATE TABLE IF NOT EXISTS rooms_comforts (
    room_id BIGINT REFERENCES rooms(room_id),
    comfort_id BIGINT REFERENCES comforts(comfort_id),
    amount INTEGER NOT NULL,
    PRIMARY KEY (room_id, comfort_id)
);