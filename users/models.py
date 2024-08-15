from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class PurchaseConfirmation(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='purchases')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {'Confirmed' if self.is_confirmed else 'Pending'}"
