# Базовый образ с Python
FROM python:3.12-slim-bullseye

# Устанавливаем переменные окружения для Python
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

# Устанавливаем рабочую директорию
WORKDIR /bestcar

# Копируем файл зависимостей в контейнер
COPY requirements.txt /bestcar/

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    netcat \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*  # Удаляем кэш и список пакетов

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в рабочую директорию
COPY . .

# Открываем порт, который будет использовать Django (по умолчанию 8000)
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]