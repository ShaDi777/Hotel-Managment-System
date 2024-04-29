CREATE TABLE IF NOT EXISTS provided_services (
    provided_service_id BIGSERIAL PRIMARY KEY,
    service_id BIGINT,
    employee_id BIGINT,
    price NUMERIC(10, 2),
    FOREIGN KEY (service_id) REFERENCES services(service_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);