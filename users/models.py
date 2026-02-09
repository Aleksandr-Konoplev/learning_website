from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email: models.EmailField

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    citi = models.CharField(max_length=50, verbose_name='Город')
    avatar = models.ImageField(
        upload_to="users/avatars/",
        default="users/avatars/default_ava.png",
        verbose_name="Аватар",
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