from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """
    Кастомная модель пользователя
    """

    email: models.EmailField
    phone_number: models.CharField
    citi: models.CharField
    avatar: models.ImageField

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(
        max_length=20, verbose_name='Номер телефона', blank=True, null=True
    )
    citi = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        default='users/avatars/default_ava.png',
        verbose_name='Аватар',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]


    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', auto_now_add=True)

    # Универсальная связь (GenericForeignKey)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип объекта')
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    paid_object = GenericForeignKey('content_type', 'object_id')

    # Параметры оплаты
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)

    # Поле для записи названия купленного товара, что бы платёж не потерялся при его удалении,
    name_paid_product = models.CharField(max_length=255, verbose_name='Название на случай удаления курса, или урока')

    def save(self, *args, **kwargs):
        if self.paid_object:
            self.name_paid_product = self.paid_object.name
        super().save(*args, **kwargs)
