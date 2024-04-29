#!/bin/bash

root="/docker-entrypoint-initdb.d"
SCHEMA="${SCHEMA:-public}"


READER_PASSWORD="${READER_PASSWORD:-reader}"
$root/roles/init_reader.sh --schema=$SCHEMA --password=$READER_PASSWORD


WRITER_PASSWORD="${WRITER_PASSWORD:-reader}"
$root/roles/init_writer.sh --schema=$SCHEMA --password=$WRITER_PASSWORD


ANALYST_PASSWORD="${ANALYST_PASSWORD:-analyst}"
ANALYST_TABLE="${ANALYST_TABLE:-reviews}"
$root/roles/init_analyst.sh --schema=$SCHEMA --table=$ANALYST_TABLE --password=$ANALYST_PASSWORD


GROUP_USERS_PASSWORDS="${GROUP_USERS_PASSWORDS:-user1:user1 bob:bob login:password}"
$root/roles/init_group.sh $GROUP_USERS_PASSWORDS