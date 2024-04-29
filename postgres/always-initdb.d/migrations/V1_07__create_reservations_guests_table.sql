CREATE TABLE IF NOT EXISTS reservations_guests (
   reservation_id BIGINT REFERENCES reservations(reservation_id), 
   guest_id BIGINT REFERENCES guests(guest_id), 
   PRIMARY KEY (reservation_id, guest_id)
);