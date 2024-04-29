0BEGIN;

-- Partition
ALTER TABLE reservations RENAME TO reservations_old;

CREATE TABLE IF NOT EXISTS reservations_master (
    reservation_id BIGSERIAL,
    room_id BIGINT REFERENCES rooms(room_id),
    check_in_date TIMESTAMP,
    check_out_date TIMESTAMP,
    PRIMARY KEY (reservation_id, check_in_date)
) PARTITION BY RANGE (check_in_date);


-- Function
create function createPartitionIfNotExists(forDate date) returns void
as $body$
    declare monthStart date := date_trunc('month', forDate);
    declare monthEndExclusive date := monthStart + interval '1 month';
    declare tableName text := 'reservations_' || to_char(forDate, 'YYYYmm');
begin
    if to_regclass(tableName) is null then
        execute format('CREATE TABLE %I PARTITION OF reservations_master FOR VALUES FROM (%L) TO (%L)', tableName, monthStart, monthEndExclusive);
        execute format('CREATE INDEX ON %I (check_in_date)', tableName);
    end if;
end;
$body$ language plpgsql;


-- Create view to delegate
create or replace view reservations as select * from reservations_master;

-- Insertion rule
create or replace rule autoCall_createPartitionIfNotExists
as on insert to reservations
do instead (
    select createPartitionIfNotExists(NEW.check_in_date::DATE);
    insert into reservations_master (reservation_id, room_id, check_in_date, check_out_date)
    values (NEW.reservation_id, NEW.room_id, NEW.check_in_date, NEW.check_out_date)
);

-- Tranfer all data
INSERT INTO reservations
SELECT * FROM reservations_old;


COMMIT;