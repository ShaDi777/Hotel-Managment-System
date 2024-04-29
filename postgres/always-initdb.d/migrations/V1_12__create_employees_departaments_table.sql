CREATE TABLE IF NOT EXISTS employees_departments (
    employee_id BIGINT,
    department_id BIGINT,
    PRIMARY KEY (employee_id, department_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);