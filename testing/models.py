from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.conf import settings


class Test(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='testing_tests')
    question = models.TextField()
    # Додайте інші поля для тестів

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    # Додайте інші поля для питань

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentTestResult(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    passed = models.BooleanField()

    def __str__(self):
        return f"{self.student.username} - {self.test.title} - {self.score}"
