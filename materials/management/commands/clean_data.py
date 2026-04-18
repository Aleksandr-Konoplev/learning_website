import os
import psycopg2
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Удаление данных с сохранением структуры таблиц (PostgreSQL)"

    def add_arguments(self, parser):
        parser.add_argument("--keep-users", action="store_true", help="Сохранить пользователей")
        parser.add_argument("--keep-courses", action="store_true", help="Сохранить курсы и уроки")
        parser.add_argument("--dry-run", action="store_true", help="Показать что будет удалено")

    def handle(self, *args, **options):
        conn = psycopg2.connect(
            host=os.getenv("HOST") or "localhost",
            database=os.getenv("NAME") or "",
            user=os.getenv("USER") or "",
            password=os.getenv("PASSWORD") or "",
            port=int(os.getenv("PORT", 5432)),
        )
        conn.autocommit = False

        try:
            with conn.cursor() as cur:
                # Получаем количество записей
                stats = {}
                for table in ["users_payment", "materials_lesson", "materials_course", "users_user"]:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    result = cur.fetchone()
                    stats[table] = result[0] if result else 0

                if options["dry_run"]:
                    self.stdout.write("=== DRY RUN ===")
                else:
                    # Очистка таблиц
                    cur.execute("TRUNCATE TABLE users_payment RESTART IDENTITY CASCADE")

                    if not options["keep_courses"]:
                        cur.execute("TRUNCATE TABLE materials_lesson RESTART IDENTITY CASCADE")
                        cur.execute("TRUNCATE TABLE materials_course RESTART IDENTITY CASCADE")

                    if not options["keep_users"]:
                        cur.execute("DELETE FROM users_user WHERE is_superuser = FALSE")

                    conn.commit()
                    self.stdout.write("Данные удалены")

                # Вывод статистики
                self.stdout.write(f"  Платежи: {stats['users_payment']}")
                if not options["keep_courses"]:
                    self.stdout.write(f"  Уроки: {stats['materials_lesson']}")
                    self.stdout.write(f"  Курсы: {stats['materials_course']}")
                if not options["keep_users"]:
                    cur.execute("SELECT COUNT(*) FROM users_user WHERE is_superuser = TRUE")
                    result = cur.fetchone()
                    superusers = result[0] if result else 0
                    regular = stats["users_user"] - superusers
                    self.stdout.write(f"  Пользователей (удалено/всего): {regular}/{stats['users_user']}")

        except Exception as e:
            conn.rollback()
            self.stdout.write(f"Ошибка: {e}")
        finally:
            conn.close()
