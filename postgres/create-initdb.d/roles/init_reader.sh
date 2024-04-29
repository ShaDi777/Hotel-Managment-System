#!/bin/bash

# Параметры по умолчанию
SCHEMA="public"
PASSWORD="reader"
ROLE="reader"


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
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO $ROLE;
    GRANT SELECT ON ALL TABLES IN SCHEMA $SCHEMA TO $ROLE;
    ALTER DEFAULT PRIVILEGES FOR ROLE $ROLE IN SCHEMA $SCHEMA
        GRANT SELECT ON TABLES TO $ROLE;
EOSQL

echo "Successfully created user: $ROLE with password: $PASSWORD"
