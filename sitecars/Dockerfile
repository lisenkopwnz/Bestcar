# Базовый образ с Python
FROM python:3.12-slim-bullseye

# Устанавливаем переменные окружения для Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /bestcar

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем системные зависимости и зависимости Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем весь код проекта в контейнер
COPY . .

# Копируем entrypoint.sh и делаем его исполнимым
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Открываем порт, который будет использовать Django (по умолчанию 8000)
EXPOSE 8000

# Устанавливаем точку входа для контейнера
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Указываем команду по умолчанию для запуска Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]