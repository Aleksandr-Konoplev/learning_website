from django.db import models


class Course(models.Model):
    """
    Модель обучающего курса, который состоит из отдельных уроков
    """

    name: models.CharField
    preview: models.ImageField
    description: models.TextField

    name = models.CharField(max_length=255, verbose_name='Курс')
    preview = models.ImageField(
        upload_to='materials/preview/',
        default='materials/preview/default_prev.png',
        verbose_name='Превью курса',
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name='Описание курса')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.name}'


class Lesson(models.Model):
    """
    Модель одного урока входящего в курс
    """

    name: models.CharField
    description: models.TextField
    preview: models.ImageField
    video_url: models.URLField
    course: models.ForeignKey

    name = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(
        upload_to='materials/preview/',
        default='materials/preview/default_prev.png',
        verbose_name='Превью урока',
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.SET_NULL,
        verbose_name='Курс',
        null=True,
        blank=True
    )
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self._meta.verbose_name}: {self.name}'
