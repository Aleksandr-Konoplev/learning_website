from django.core.management import BaseCommand, call_command
from users.models import User


class Command(BaseCommand):
    help = 'Загружает фикстуру и хэширует пароли пользователей'

    def add_arguments(self, parser):
        parser.add_argument(
            'fixture',
            nargs='?',
            default='fixtures/test_data.json',
            help='Путь к файлу фикстуры (по умолчанию: fixtures/test_data.json)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Загрузка групп...')
        call_command('loaddata', 'fixtures/groups.json')
        self.stdout.write(self.style.SUCCESS('Группы загружены успешно'))

        fixture_path = options['fixture']

        self.stdout.write(f'Загрузка фикстуры: {fixture_path}')
        call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('Фикстура загружена успешно'))

        self.stdout.write('Хэширование паролей пользователей...')
        users = User.objects.all()
        hashed_count = 0

        for user in users:
            password = user.password

            if password and not password.startswith(('pbkdf2_', 'argon2', 'bcrypt', 'sha256_', 'sha1', 'md5')):
                plain_password = password
                user.set_password(plain_password)
                user.save()
                hashed_count += 1
                self.stdout.write(f'  Пароль хэширован для: {user.email}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Хэширование завершено. Обработано пользователей: {hashed_count}'
            )
        )
