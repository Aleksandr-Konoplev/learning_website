# Learning Website

Простой проект на Django для обучения.

## Структура проекта

```
learning_website/
├── config/                # Конфигурация Django
│   ├── __init__.py
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # Маршруты URL
│   ├── wsgi.py            # WSGI конфигурация
│   └── asgi.py            # ASGI конфигурация
├── manage.py              # Django management script
├── pyproject.toml         # Зависимости Poetry
├── requirements.txt       # Зависимости pip
├── poetry.lock            # Lock файл Poetry
└── .env                   # Переменные окружения (не в git)

```

## Требования

- Python >= 3.14
- PostgreSQL
- Poetry (для управления зависимостями)

## Установка

1. Клонировать репозиторий:
   ```bash
   git clone <url>
   cd learning_website
   ```

2. Установить зависимости:
   ```bash
   poetry install
   ```

3. Создать файл `.env`:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   NAME=your-db-name
   USER=your-db-user
   PASSWORD=your-db-password
   HOST=localhost
   PORT=5432
   ```

4. Применить миграции:
   ```bash
   python manage.py migrate
   ```

## Запуск

```bash
python manage.py runserver
```

Сервер запустится на http://127.0.0.1:8000/

## Технологии

- Django 6.x
- Django REST Framework
- PostgreSQL
- Poetry
