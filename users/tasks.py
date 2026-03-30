from users.services import send_mail_subscribe
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def task_update(email_list, course_name):
    """Действия при обновлении курса"""
    message = f"В курсе {course_name} произошли изменения, скорее посмотрите, там что-то интересное"
    send_mail_subscribe(email_list, message=message)


@shared_task
def block_user():

    # Рассчитать дату 30 дней назад
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Найти активных пользователей, не заходивших 30+ дней
    inactive_users = User.objects.filter(is_active=True, last_login__lt=thirty_days_ago)

    # Заблокировать пользователей
    count = inactive_users.update(is_active=False)

    return f"Заблокировано {count} пользователей"


@shared_task
def test_task():
    print("test task")
