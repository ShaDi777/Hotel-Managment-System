#!/bin/bash

root="/always-initdb.d"
script_path="$root/backups/create_backup.sh"
while true; do
    echo "Executing $script_path"
    bash "$script_path"
    
    sleep 60
done
