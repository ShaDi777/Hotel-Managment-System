CREATE TABLE IF NOT EXISTS reviews (
   reservation_id BIGINT,
   guest_id BIGINT,
   rating NUMERIC(3, 2), 
   comment TEXT, 
   review_date TIMESTAMP,
   PRIMARY KEY (reservation_id, guest_id),
   FOREIGN KEY (reservation_id, guest_id) REFERENCES reservations_guests(reservation_id, guest_id)
);