# Learning Website

Проект на Django, обучающая платформа

## Структура проекта

```
learning_website/
├── config/                # Конфигурация Django
│   ├── __init__.py
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # Маршруты URL
│   ├── wsgi.py            # WSGI конфигурация
│   └── asgi.py            # ASGI конфигурация
├── users/                 # Приложение пользователей
│   ├── __init__.py
│   ├── admin.py           # Админка пользователей
│   ├── apps.py            # Конфигурация приложения
│   ├── models.py          # Модели пользователей
│   ├── serializers.py     # Сериализаторы API
│   ├── urls.py            # URL маршруты
│   ├── views.py           # Представления API
│   └── tests.py           # Тесты
├── materials/             # Приложение материалов (курсы, уроки)
│   ├── __init__.py
│   ├── admin.py           # Админка материалов
│   ├── apps.py            # Конфигурация приложения
│   ├── models.py          # Модели курсов и уроков
│   ├── serializers.py     # Сериализаторы API
│   ├── urls.py            # URL маршруты
│   ├── views.py           # Представления API
│   └── tests.py           # Тесты
├── media/                 # Медиафайлы
│   ├── users/avatars/     # Аватары пользователей
│   └── materials/preview/ # Превью материалов
├── fixtures/              # Фикстуры для тестовых данных
│   └── test_data.json
├── manage.py              # Django management script
├── pyproject.toml         # Зависимости Poetry
├── requirements.txt       # Зависимости pip
├── poetry.lock            # Lock файл Poetry
├── .env.example           # Пример переменных окружения
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
   HOST=127.0.0.1
   PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_DB=learning_website
   POSTGRES_PASSWORD=
   ```

4. Применить миграции:
   ```bash
   python manage.py migrate
   ```
   
5. Добавить тестовые значения в базу данных:
   ```bash
   python manage.py load_test_data
   ```

## Кастомные команды
1. Полная очистка БД (включая схемы, после команды необходимо применить миграции)
   ```bash
   python manage.py full_clean
   ```
2. Очистка данных БД (все таблицы и взаимосвязи остаются)
   ```bash
   python manage.py clean_data
   ```

## Запуск

```bash
python manage.py runserver
```

Сервер запустится на http://127.0.0.1:8000/

---

## Установка на виртуальную машину



## API Эндпоинты

### Admin
- `GET /admin/` - Админ панель Django

### Materials API (`/materials/`)

#### Курсы
- `GET /materials/` - Список всех курсов
- `POST /materials/` - Создать новый курс
- `GET /materials/<id>/` - Получить курс по ID
- `PUT /materials/<id>/` - Полностью обновить курс
- `PATCH /materials/<id>/` - Частично обновить курс
- `DELETE /materials/<id>/` - Удалить курс

#### Уроки
- `GET /materials/lessons/` - Список всех уроков
- `POST /materials/lesson/create/` - Создать новый урок
- `GET /materials/lesson/<id>/` - Получить урок по ID
- `PUT /materials/lesson/<id>/update/` - Обновить урок
- `PATCH /materials/lesson/<id>/update/` - Частично обновить урок
- `DELETE /materials/lesson/<id>/delete/` - Удалить урок

### Users API (`/users/`)

#### Платежи
- `users/payments/` - Список всех платежей
- `users/payments/?content_type__model=<name_model>` - Список отфильтрованный по модели
- `users/payments/?content_type__model=<name_model>&object_id=<id>` - Список отфильтрованный по объекту модели

#### Подписки
- `users/subscriptions/` - Подписаться / Отписаться

#### Пользователи
- `GET /users/list/` - Список всех пользователей
- `POST /users/` - Создать нового пользователя
- `GET /users/{id}/` - Получить пользователя по ID
- `PUT /users/{id}/` - Полностью обновить пользователя
- `PATCH /users/{id}/` - Частично обновить пользователя
- `DELETE /users/{id}/` - Удалить пользователя

## Технологии

- Python 3.14+
- Django 6.x
- Django REST Framework
- Django filter 25.2
- PostgreSQL (psycopg2)
- Pillow (обработка изображений)
- Poetry (управление зависимостями)
- python-dotenv (переменные окружения)

### Инструменты разработки

- Black (форматирование кода)
- isort (сортировка импортов)
- flake8 (статический анализ)
- mypy (проверка типов)
