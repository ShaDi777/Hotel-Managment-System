#!/bin/bash

ROLE="manipulator"

# Проверка переменных окружения
if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ]; then
    echo "Environment POSTGRES_DB and POSTGRES_USER not found."
    exit 1
fi


# Создание роли
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE $ROLE;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $ROLE;
EOSQL


# Проверяем количество переданных аргументов
if [ "$#" -eq 0 ]; then
    echo "No user:password specified." >&2
    exit 1
fi


# Перебираем переданные пользователей и пароли
for user_pass in "$@"; do
    IFS=':' read -r username password <<< $user_pass

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $username WITH PASSWORD '$password';
        GRANT $ROLE TO $username;
EOSQL

    echo "Successfully created $ROLE: $username with password: $password"
done