from django.db import models


class Discount(models.Model):
    course_count = models.PositiveIntegerField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return f"{self.discount_percentage}% off on {self.course_count} courses"

