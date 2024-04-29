# hotel/postgres:16
FROM postgres:16

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=hotel
ENV VERSION=V2_02
ENV BACKUP_PERIOD_HOURS=1
ENV BACKUP_MAX_AMOUNT=3

COPY ./create-initdb.d /docker-entrypoint-initdb.d
COPY ./always-initdb.d /always-initdb.d
COPY ./custom-entrypoint.sh /usr/local/bin/custom-entrypoint.sh
COPY ./.backups /.backups

ENTRYPOINT ["bash", "/usr/local/bin/custom-entrypoint.sh", "postgres"]