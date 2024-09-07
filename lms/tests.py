from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, Subscribe
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='tsoy@gmail.com')

        self.course = Course.objects.create(title='Course',
                                            description='Course',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson',
                                            description='Lesson',
                                            owner=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('lms:lesson_create')
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson',
            'course': self.course.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            'title': 'New Lesson 2',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'New Lesson 2')

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        url = reverse('lms:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'title': self.lesson.title,
             'description': self.lesson.description, 'image': None,
             'url': None, 'course': self.lesson.course.pk,
             'owner': self.lesson.owner.pk}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='tsoy@gmail.com')
        self.course = Course.objects.create(title='Course',
                                            description='Course',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_create(self):
        url = reverse('lms:subscribe_create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscribe.objects.all().count(), 1)
        self.assertEqual(response.json(),
                         {"message": "Subscribe created successfully"})

    def test_subscribe_delete(self):
        Subscribe.objects.create(course=self.course, user=self.user)
        url = reverse('lms:subscribe_create')
        data = {'course': self.course.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscribe.objects.all().count(), 0)
        self.assertEqual(response.json(),
                         {"message": "Subscribe deleted successfully"})
