from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Використання get_user_model() для роботи з кастомною моделлю користувача
User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        abstract = True  # Встановлює, що це абстрактна модель, і вона не буде створена як окрема таблиця в базі даних.

    def __str__(self):
        return self.title


class ConcreteProduct(Product):
    pass


class PhysicalProduct(Product):
    weight = models.DecimalField(max_digits=5, decimal_places=2)


class DigitalProduct(Product):
    download_link = models.URLField()


class Course(Product):
    teacher = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'Teachers'},
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_tests')
    question = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Електронна пошта")
    rating = models.IntegerField(verbose_name="Оцінка", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class DemoMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='demo_materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.title