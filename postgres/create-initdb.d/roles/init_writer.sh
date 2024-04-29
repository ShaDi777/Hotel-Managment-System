#!/bin/bash

# Параметры по умолчанию
SCHEMA="public"
PASSWORD="writer"
ROLE="writer"


# Проверка переменных окружения
if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ]; then
    echo "Environment POSTGRES_DB and POSTGRES_USER not found."
    exit 1
fi


# Прочитать переданные аргументы
source argument_parser.sh
extract_arguments "$@"


# Создание роли
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE $ROLE WITH LOGIN PASSWORD '$PASSWORD';
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA $SCHEMA TO $ROLE;
    GRANT USAGE ON SCHEMA public TO writer;
    ALTER DEFAULT PRIVILEGES FOR ROLE $ROLE IN SCHEMA $SCHEMA
        GRANT SELECT, INSERT, UPDATE ON TABLES TO $ROLE;
EOSQL

echo "Successfully created user: $ROLE with password: $PASSWORD"
