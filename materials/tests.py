from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from materials.models import Course, Lesson


class LessonTestCase(APITestCase):
    """ Тесты CRUD операций над моделью Lesson """
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

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": 'http://testserver/media/materials/preview/default_prev.png',
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user_owner.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'name': 'Test create lesson',
            'owner': self.user_owner.pk,
            'description': 'Test description',
            'course': self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'Test update lesson',
            'description': 'Test update description'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Test update lesson')

    def test_lesson_destroy(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_moder_create(self):
        """ Попытка создания урока модератором """
        self.client.force_authenticate(user=self.user_moder)
        url = reverse('materials:lesson_create')
        data = {
            'name': 'Test create lesson by moderator',
            'owner': self.user_moder.pk,
            'description': 'Test description',
            'course': self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_moder_destroy(self):
        """ Попытка удаления урока модератором """
        self.client.force_authenticate(user=self.user_moder)
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        # Модератор может удалять только свои уроки, этот урок принадлежит user_owner
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_course_subscription(self):
        """ Тестирование подписки / отписки на курс """
        self.client.force_authenticate(user=self.user_default)
        url = reverse('users:user_subscriptions')
        data = {'course_id': self.course.pk}

        # Подписка
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'подписка добавлена')

        # Отписка
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'подписка удалена')

