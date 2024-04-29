CREATE INDEX IF NOT EXISTS employees_departments_department_id_fkey
ON employees_departments (department_id);


CREATE INDEX IF NOT EXISTS reservations_room_id_check_dates_idx
ON reservations (room_id, check_in_date, check_out_date);


CREATE INDEX IF NOT EXISTS reservations_guests_guest_id_fkey
ON reservations_guests (guest_id);


CREATE INDEX IF NOT EXISTS reviews_reservation_id_fkey
ON reviews (reservation_id);
CREATE INDEX IF NOT EXISTS reservations_room_id_fkey
ON reservations (room_id);


CREATE INDEX IF NOT EXISTS rooms_comforts_comfort_id_amount_idx
ON rooms_comforts (comfort_id, amount);
