CREATE TABLE IF NOT EXISTS employees_positions (
    employee_id BIGINT,
    position_id BIGINT,
    PRIMARY KEY (employee_id, position_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);