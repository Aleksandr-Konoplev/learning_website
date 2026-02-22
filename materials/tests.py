from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from materials.models import Course, Lesson


class LessonTestCase(APITestCase):
    client: APIClient

    def setUp(self):
        # Пользователь-модератор
        self.user_moder = User.objects.create(email='moder@mail.ru', password='TestPass123')
        # Обычный пользователь
        self.user_default = User.objects.create(email='user@mail.ru', password='TestPass123')
        # Пользователь-владелец
        self.user_owner = User.objects.create(email='owner@mail.ru', password='TestPass123')

        # Получает или создает группу с именем 'moders'
        self.group_moder, _ = self.user_moder.groups.get_or_create(name='moders')
        # Добавляет пользователя-модератора в группу 'moders'
        self.user_moder.groups.add(self.group_moder)

        # Добавляем курс
        self.course = Course.objects.create(name='Test course', owner=self.user_owner)
        # Добавляем урок
        self.lesson = Lesson.objects.create(name='Test lesson', course=self.course, owner=self.user_owner)

        self.client.force_authenticate(user=self.user_owner)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test lesson')
        self.assertEqual(data.get('course'), self.course.pk)

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'name': 'Test create lesson',
            'owner': self.user_owner.pk,
            'description': 'Test description',
            'course': self.course.pk
        }
        response = self.client.post(url, data)

        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # self.assertEqual(Lesson.objects.all().count(), 2)





    # def test_lesson_delete(self):
    #     url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Lesson.objects.all().count(), 0)
