import psycopg2
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    """
    Команда для ПОЛНОЙ очистки PostgreSQL базы данных.
    Удаляет все таблицы из БД - данные, связи, индексы, constraints.
    Использует прямое подключение через psycopg2.
    """
    help = 'ПОЛНАЯ очистка PostgreSQL БД - удаление всех таблиц с данными и связями'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_true',
            help='Не запрашивать подтверждение',
        )
        parser.add_argument(
            '--exclude',
            nargs='+',
            type=str,
            help='Список таблиц для исключения из удаления',
        )
        parser.add_argument(
            '--exclude-auth',
            action='store_true',
            help='Исключить системные таблицы auth_* и django_*',
        )

    def handle(self, *args, **options):
        db_config = self._get_db_config()
        self._validate_environment(options)

        with self._connect(db_config) as connection:
            tables_to_drop = self._get_tables_to_drop(connection, options)

            if not tables_to_drop:
                self.stdout.write('Нет таблиц для удаления')
                return

            self._confirm_deletion(options, tables_to_drop)
            self._drop_tables(connection, tables_to_drop)
            self._print_success(tables_to_drop)

    def _get_db_config(self):
        """Получает конфигурацию базы данных из Django settings."""
        db = settings.DATABASES['default']

        if 'postgresql' not in db['ENGINE']:
            raise CommandError(
                f"Команда работает только с PostgreSQL. "
                f"Текущий ENGINE: {db['ENGINE']}"
            )

        return {
            'dbname': db['NAME'],
            'user': db['USER'],
            'password': db['PASSWORD'],
            'host': db['HOST'],
            'port': db['PORT'] or '5432',
        }

    def _connect(self, db_config):
        """Создает подключение к PostgreSQL через psycopg2."""
        try:
            self.stdout.write(f"Подключение к БД: {db_config['dbname']}@{db_config['host']}")
            return psycopg2.connect(**db_config)
        except psycopg2.Error as e:
            raise CommandError(f"Ошибка подключения к БД: {e}")

    def _validate_environment(self, options):
        """Проверяет окружение (production)."""
        if not settings.DEBUG and not options['noinput']:
            self.stdout.write(
                'ВНИМАНИЕ! Вы запускаете команду в production режиме (DEBUG=False)'
            )
            raise CommandError(
                'Операция отменена. Используйте --noinput только если уверены.'
            )

    def _get_tables_to_drop(self, connection, options):
        """Возвращает список таблиц для удаления."""
        exclude_tables = options['exclude'] or []

        if options['exclude_auth']:
            exclude_tables.extend(self._get_auth_tables())

        all_tables = self._get_all_tables(connection)

        return [table for table in all_tables if table not in exclude_tables]

    def _get_auth_tables(self):
        """Возвращает список системных таблиц Django auth."""
        return [
            'auth_group', 'auth_group_permissions', 'auth_permission',
            'auth_user', 'auth_user_groups', 'auth_user_user_permissions',
            'django_admin_log', 'django_content_type', 'django_migrations',
            'django_session'
        ]

    def _get_all_tables(self, connection):
        """Получает список всех таблиц из PostgreSQL."""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """)
            return [row[0] for row in cursor.fetchall()]

    def _confirm_deletion(self, options, tables):
        """Запрашивает подтверждение удаления."""
        if options['noinput']:
            return

        self.stdout.write('=' * 60)
        self.stdout.write('ВНИМАНИЕ! ПОЛНОЕ УДАЛЕНИЕ БАЗЫ ДАННЫХ')
        self.stdout.write('=' * 60)
        self.stdout.write('')
        self.stdout.write('Будут удалены ВСЕ таблицы со следующими данными:')
        self.stdout.write('  - Пользователи (users_user)')
        self.stdout.write('  - Платежи (users_payment)')
        self.stdout.write('  - Курсы (materials_course)')
        self.stdout.write('  - Уроки (materials_lesson)')
        self.stdout.write('  - Все связи, индексы и constraints')
        self.stdout.write('')
        self.stdout.write(f'Найдено таблиц для удаления: {len(tables)}')
        self.stdout.write('')
        self.stdout.write('ВНИМАНИЕ: Эту операцию НЕВОЗМОЖНО отменить!')
        self.stdout.write('')

        confirm = input('Введите "Yes" для подтверждения: ')
        if confirm != 'Yes':
            raise CommandError('Операция отменена.')

    def _drop_tables(self, connection, tables):
        """Удаляет указанные таблицы."""
        self.stdout.write('Начинаю полное удаление таблиц...')

        with connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
                    self.stdout.write(f'  Удалена таблица: {table}')
                except psycopg2.Error as e:
                    self.stdout.write(f'  Ошибка удаления {table}: {e}')

        connection.commit()

    def _print_success(self, tables):
        """Выводит сообщение об успешном завершении."""
        self.stdout.write('')
        self.stdout.write(f'База данных полностью очищена!')
        self.stdout.write(f'  Удалено таблиц: {len(tables)}')
        self.stdout.write('')
        self.stdout.write('Для восстановления структуры выполните:')
        self.stdout.write('  python manage.py migrate')
