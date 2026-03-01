from users.services import send_mail_subscribe
from celery import shared_task

@shared_task
def task_update(email_list, course_name):
    """ Действия при обновлении курса """
    message = f'В курсе {course_name} произошли изменения, скорее посмотрите, там что-то интересное'
    send_mail_subscribe(email_list, message=message)


@shared_task
def block_user():
    # Если 30 дней не входил деактивировать пользователей (Не по одному!!! По иодному плохо)
    pass


@shared_task
def test_task():
    print('test task')
