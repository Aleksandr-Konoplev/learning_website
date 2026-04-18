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
- Docker
- Docker Compose plugin

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

## Запуск через Docker Compose

1. Создать файл `.env` на основе шаблона:
   ```bash
   cp .env.example .env
   ```

2. Запустить проект одной командой:
   ```bash
   docker compose up -d --build
   ```

3. Проверить состояние контейнеров:
   ```bash
   docker compose ps
   ```

4. При необходимости посмотреть логи:
   ```bash
   docker compose logs web --tail=100
   ```

После запуска приложение должно быть доступно по адресу `http://127.0.0.1`.

### Состав сервисов Docker Compose

- `web` - Django
- `db` - PostgreSQL
- `redis` - Redis
- `celery` - Celery worker
- `celery-beat` - Celery Beat scheduler
- `nginx` - Nginx

---

## Установка на виртуальную машину

1. Подключиться к серверу по SSH:
   ```bash
   ssh <user>@<server_ip>
   ```

2. Установить Docker, Compose plugin и Git, если они еще не установлены:
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose-plugin git
   sudo systemctl enable --now docker
   ```

3. Клонировать репозиторий на сервер:
   ```bash
   git clone -b <имя ветки> git@github.com:Aleksandr-Konoplev/learning_website.git
   cd learning_website
   ```

4. Создать файл `.env` на основе шаблона:
   ```bash
   cp .env.example .env
   ```

5. Заполнить `.env` актуальными значениями:
   ```env
   SECRET_KEY=<django-secret-key>
   DEBUG=True
   HOST=127.0.0.1
   PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_DB=learning_website
   POSTGRES_PASSWORD=<postgres-password>
   STRIPE_API_KEY=<stripe-api-key>
   EMAIL_HOST=smtp.yandex.ru
   EMAIL_PORT=465
   EMAIL_USE_TLS=False
   EMAIL_USE_SSL=True
   EMAIL_HOST_USER=<email-login>
   EMAIL_HOST_PASSWORD=<email-password>
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://<server_ip>
   ```

6. Собрать и запустить контейнеры:
   ```bash
   sudo docker compose up -d --build
   ```

7. Проверить состояние сервисов:
   ```bash
   sudo docker compose ps
   sudo docker compose logs web --tail=100
   ```

8. Проверить доступность приложения с сервера:
   ```bash
   curl -I http://127.0.0.1
   ```
   После запуска приложение должно быть доступно по адресу `http://<server_ip>`.

9. Для обновления проекта на сервере:
   ```bash
   git pull origin main
   docker compose up -d --build
   ```

## CI/CD

В репозитории настроен GitHub Actions workflow `.github/workflows/ci.yml`, который:

1. Запускает линтинг `flake8`
2. Запускает тесты Django
3. Проверяет сборку Docker-образов
4. При успешных проверках выполняет деплой на сервер по SSH

## Настройка SSH-доступа для деплоя

1. Сгенерировать SSH-ключ для GitHub Actions:
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f github_actions_deploy
   ```

2. Добавить публичный ключ `github_actions_deploy.pub` на сервер в файл `~/.ssh/authorized_keys`

3. Добавить приватный ключ `github_actions_deploy` в GitHub Secrets

## GitHub Secrets для деплоя

Необходимо создать следующие Secrets в репозитории GitHub:

- `SERVER_HOST` - IP-адрес или домен сервера
- `SERVER_PORT` - SSH-порт сервера
- `SERVER_USER` - пользователь для SSH-подключения
- `SERVER_SSH_KEY` - приватный SSH-ключ для деплоя
- `SERVER_APP_DIR` - путь до проекта на сервере

## Автоматический деплой

После `push` в ветку `main` GitHub Actions:

1. Проверяет код
2. Подключается к серверу по SSH
3. Обновляет проект из репозитория
4. Выполняет команду:
   ```bash
   docker compose up -d --build
   ```

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
