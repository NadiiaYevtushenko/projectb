from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Course, Review, Video, Test
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ConcreteProduct
from django.core import mail
from courses.tasks import send_notification_email


# Модульний тест (Unit Test)
class CourseModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='teacher', password='testpass')

    def test_course_str(self):
        course = Course.objects.create(title="Test Course", duration=10, teacher=self.user)
        self.assertEqual(str(course), "Test Course")


#Функціональний тест
class CourseListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='teacher', password='testpass')
        Course.objects.create(title="Test Course 1", duration=10, teacher=self.user)
        Course.objects.create(title="Test Course 2", duration=15, teacher=self.user)

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course 1")
        self.assertContains(response, "Test Course 2")


#Інтеграційний тест
class CourseDetailIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='teacher', password='testpass')
        self.course = Course.objects.create(title="Test Course", duration=10, teacher=self.user)
        self.video1 = Video.objects.create(title="Video 1", video_url="http://example.com/video1", course=self.course)
        self.video2 = Video.objects.create(title="Video 2", video_url="http://example.com/video2", course=self.course)
        self.test1 = Test.objects.create(title="Test 1", course=self.course, question="What is Django?")
        self.test2 = Test.objects.create(title="Test 2", course=self.course, question="What is Python?")

    def test_course_detail_view(self):
        url = reverse('course_detail', args=[self.course.pk])
        response = self.client.get(url)

        # Перевірка статусу відповіді
        self.assertEqual(response.status_code, 200)

        # Перевірка наявності назви курсу
        self.assertContains(response, "Test Course")

        # Перевірка наявності відеоуроків у контексті
        self.assertIn('lessons', response.context)
        self.assertEqual(len(response.context['lessons']), 2)
        self.assertEqual(response.context['lessons'][0].title, "Video 1")
        self.assertEqual(response.context['lessons'][1].title, "Video 2")

        # Перевірка наявності тестів у контексті
        self.assertIn('tests', response.context)
        self.assertEqual(len(response.context['tests']), 2)
        self.assertEqual(response.context['tests'][0].title, "Test 1")
        self.assertEqual(response.context['tests'][1].title, "Test 2")


# Функціональний тест для REST API
class ConcreteProductAPITest(APITestCase):
    def setUp(self):
        self.product = ConcreteProduct.objects.create(title="Test Product", price=100)

    def test_get_concrete_product_list(self):
        url = reverse('concreteproduct-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Product")


#Celery
class TasksTestCase(TestCase):
    def test_send_notification_email(self):
        # Проста перевірка запуску завдання
        result = send_notification_email.delay('Test Subject', 'Test message', ['to@example.com'])
        self.assertIsNotNone(result.id)