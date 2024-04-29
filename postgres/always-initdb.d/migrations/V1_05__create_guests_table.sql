CREATE TABLE IF NOT EXISTS guests (
    guest_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(25),
    address VARCHAR(255)
);