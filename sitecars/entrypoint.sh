#!/bin/bash

# Ожидание запуска PostgreSQL
echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."
timeout=240

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: PostgreSQL не запустился за ожидаемое время."
        exit 1
    fi
done

echo "PostgreSQL доступен. Выполняю сборку статических файлов..."

# Сборка статических файлов
if ! python manage.py collectstatic --no-input; then
    echo "Ошибка: Не удалось собрать статические файлы"
    exit 1
fi

# Автоматическое создание миграций и их применение
echo "Применяю миграции..."
if ! python manage.py makemigrations; then
    echo "Ошибка: Не удалось создать миграции"
    exit 1
fi

if ! python manage.py migrate; then
    echo "Ошибка: Не удалось применить миграции"
    exit 1
fi

# Временная задержка перед созданием индекса в Elasticsearch (4 минуты)
echo "Ожидаю 4 минуты перед созданием индекса в Elasticsearch..."
sleep 240

# Ожидание запуска Redis
echo "Ожидание запуска Redis на $REDIS_HOST:$REDIS_PORT..."
timeout=120
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: Redis не запустился за ожидаемое время."
        exit 1
    fi
done

echo "Redis доступен."

# Создание индекса в Elasticsearch
echo "Создаю индекс в Elasticsearch..."
if ! python manage.py search_index --create; then
    echo "Ошибка: Не удалось создать индекс в Elasticsearch"
    exit 1
fi

# Запуск Celery вручную
echo "Запускаю Celery..."
celery -A sitecars worker --loglevel=info &

# Запускаем приложение Django
exec "$@"