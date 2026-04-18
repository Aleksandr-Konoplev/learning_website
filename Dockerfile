FROM python:3.14-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Отключаем .pyc и включаем немедленный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости для psycopg2 и сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем проект в контейнер
COPY . .

# Открываем порт приложения
EXPOSE 8000
