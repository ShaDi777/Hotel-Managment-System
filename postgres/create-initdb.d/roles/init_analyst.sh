#!/bin/bash

# Параметры по умолчанию
SCHEMA="public"
TABLE=""
PASSWORD="analyst"
ROLE="analyst"


# Проверка переменных окружения
if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ]; then
    echo "Environment POSTGRES_DB and POSTGRES_USER not found."
    exit 1
fi

# Прочитать переданные аргументы
source argument_parser.sh
extract_arguments_analyst "$@"

if [ -z "$TABLE" ]; then
    echo "No table specified."
    exit 1
fi

# Создание роли
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE $ROLE WITH LOGIN PASSWORD '$PASSWORD';
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO $ROLE;
    GRANT SELECT ON $SCHEMA.$TABLE TO $ROLE;
EOSQL

echo "Successfully created user: $ROLE with password: $PASSWORD"
