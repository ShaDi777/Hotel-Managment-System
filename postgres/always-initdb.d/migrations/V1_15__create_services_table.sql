CREATE TABLE IF NOT EXISTS services (
    service_id BIGSERIAL PRIMARY KEY,
    service_name VARCHAR(255),
    description TEXT
);