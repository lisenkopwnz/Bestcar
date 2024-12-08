#!/bin/bash

# �������� ������� PostgreSQL
echo "�������� ������� PostgreSQL �� $DB_HOST:$DB_PORT..."
timeout=240

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "������: PostgreSQL �� ���������� �� ��������� �����."
        exit 1
    fi
done

echo "PostgreSQL ��������. �������� ������ ����������� ������..."

# ������ ����������� ������
if ! python manage.py collectstatic --no-input; then
    echo "������: �� ������� ������� ����������� �����"
    exit 1
fi

# �������������� �������� �������� � �� ����������
echo "�������� ��������..."
if ! python manage.py makemigrations; then
    echo "������: �� ������� ������� ��������"
    exit 1
fi

if ! python manage.py migrate; then
    echo "������: �� ������� ��������� ��������"
    exit 1
fi

# ��������� �������� ����� ��������� ������� � Elasticsearch (4 ������)
echo "������ 4 ������ ����� ��������� ������� � Elasticsearch..."
sleep 240

# �������� ������� Redis
echo "�������� ������� Redis �� $REDIS_HOST:$REDIS_PORT..."
timeout=120
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "������: Redis �� ���������� �� ��������� �����."
        exit 1
    fi
done

echo "Redis ��������."

# �������� ������� � Elasticsearch
echo "������ ������ � Elasticsearch..."
if ! python manage.py search_index --create; then
    echo "������: �� ������� ������� ������ � Elasticsearch"
    exit 1
fi

# ������ Celery �������
echo "�������� Celery..."
celery -A sitecars worker --loglevel=info &

# ��������� ���������� Django
exec "$@"