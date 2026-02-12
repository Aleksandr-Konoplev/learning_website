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
   
5. Добавить тестовые значения в базу данных:
   ```bash
   python manage.py loaddata users/fixtures/test_data.json
   ```

## Запуск

```bash
python manage.py runserver
```

Сервер запустится на http://127.0.0.1:8000/

## API Эндпоинты

### Admin
- `GET /admin/` - Админ панель Django

### Materials API (`/materials/`)

#### Курсы
- `GET /materials/` - Список всех курсов
- `POST /materials/` - Создать новый курс
- `GET /materials/{id}/` - Получить курс по ID
- `PUT /materials/{id}/` - Полностью обновить курс
- `PATCH /materials/{id}/` - Частично обновить курс
- `DELETE /materials/{id}/` - Удалить курс

#### Уроки
- `GET /materials/lessons/` - Список всех уроков
- `POST /materials/lesson/create/` - Создать новый урок
- `GET /materials/lesson/{id}/` - Получить урок по ID
- `PUT /materials/lesson/{id}/update/` - Обновить урок
- `PATCH /materials/lesson/{id}/update/` - Частично обновить урок
- `DELETE /materials/lesson/{id}/delete/` - Удалить урок

### Users API (`/users/`)

#### Пользователи
- `GET /users/` - Список всех пользователей
- `POST /users/` - Создать нового пользователя
- `GET /users/{id}/` - Получить пользователя по ID
- `PUT /users/{id}/` - Полностью обновить пользователя
- `PATCH /users/{id}/` - Частично обновить пользователя
- `DELETE /users/{id}/` - Удалить пользователя

## Технологии

- Django 6.x
- Django REST Framework
- PostgreSQL
- Poetry
