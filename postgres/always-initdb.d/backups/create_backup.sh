#!/bin/bash

# Restore from backup
# psql -f /always-initdb.d/backups/save/backup_1.1million.sql -U postgres

# Create folder for backups
root="/always-initdb.d"
save_dir="$root/backups/save"
mkdir -p $save_dir

create_new_backup() {
    # Create backup
    backup_file="$save_dir/backup_`date +%Y-%m-%d"_"%H-%M`.sql"
    pg_dumpall -c -U postgres > $backup_file

    [ -s $backup_file ] && echo "Success backup" || rm $backup_file

    # Remove oldest backups if necessary
    BACKUP_MAX_AMOUNT="${BACKUP_MAX_AMOUNT:-2}"
    while [[ $(ls "$save_dir" -1 | wc -l) -gt $BACKUP_MAX_AMOUNT ]]; do
        rm $(ls $save_dir | sort -n | head -1 | sed -e "s|^|$save_dir/|")
    done
}

calculate_age_in_hours() {
    local file="$1"
    local current_time=$(date +%s)
    local file_date=$(echo "$file" | sed 's/\./_/g'  | cut -d '_' -f 2 )
    local file_time=$(echo "$file" | sed 's/\./_/g'  | cut -d '_' -f 3 | sed 's/-/:/g')
    local file_datetime=$(date -d "$file_date $file_time" +%s)
    local age=$(( ($current_time - $file_datetime) / 3600 ))
    echo "$age"
}

# Check if it's time to create a new backup
BACKUP_PERIOD_HOURS="${BACKUP_PERIOD_HOURS:-24}"
latest_backup=$(ls -1t "$save_dir" | grep '^backup_' | head -n1)
if [ -z "$latest_backup" ]; then
    create_new_backup
else
    hours_since_last_backup=$(calculate_age_in_hours "$latest_backup")
    echo $hours_since_last_backup
    if [ "$hours_since_last_backup" -ge "$BACKUP_PERIOD_HOURS" ]; then
        create_new_backup
    fi
fi
