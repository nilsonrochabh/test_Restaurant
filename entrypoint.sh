#!/bin/sh

# entrypoint.sh - versão sem netcat

echo "Aguardando PostgreSQL estar pronto..."

# Aguarda o banco de dados usando psycopg2/python
until python -c "
import sys
import psycopg2
from psycopg2 import OperationalError
from time import sleep

for i in range(30):
    try:
        conn = psycopg2.connect(
            dbname='${DB_NAME}',
            user='${DB_USER}',
            password='${DB_PASSWORD}',
            host='${DB_HOST}',
            port='${DB_PORT}'
        )
        conn.close()
        print('PostgreSQL está pronto!')
        sys.exit(0)
    except OperationalError:
        if i == 29:
            print('PostgreSQL não ficou pronto a tempo')
            sys.exit(1)
        sleep(1)
"
do
  sleep 1
done

echo "PostgreSQL iniciado!"

# Executa migrações
python manage.py migrate --noinput

# Coleta arquivos estáticos (se houver)
python manage.py collectstatic --noinput

# Inicia a aplicação
exec "$@"