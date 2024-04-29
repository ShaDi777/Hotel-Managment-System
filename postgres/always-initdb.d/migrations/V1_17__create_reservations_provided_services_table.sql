CREATE TABLE IF NOT EXISTS reservations_provided_services (
    reservation_service_id BIGSERIAL PRIMARY KEY,
    provided_service_id BIGINT,
    reservation_id BIGINT,
    request_date TIMESTAMP,
    FOREIGN KEY (provided_service_id) REFERENCES provided_services(provided_service_id),
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
);