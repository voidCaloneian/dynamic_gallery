#!/bin/bash
set -e

echo "Создаём миграции"
python manage.py makemigrations photos --noinput

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Запускаем Gunicorn..."
exec gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000