from users.services import send_mail_subscribe
from celery import shared_task

@shared_task
def task_update(email_list):
    """ Уведомить об обновлении подписчиков """
    # Вызвать рассылку
    pass


@shared_task
def block_user():
    # Если 30 дней не входил деактивировать пользователей (Не по одному!!! По иодному плохо)
    pass