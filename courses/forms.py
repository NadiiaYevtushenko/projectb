from django import forms
from .models import Review, Course


class ReviewForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Виберіть курс", label="Курс")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Виберіть курс", label="Курс")

    RATING_CHOICES = [
        (1, '1 - Дуже погано'),
        (2, '2 - Погано'),
        (3, '3 - Нормально'),
        (4, '4 - Добре'),
        (5, '5 - Відмінно'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, label="Рейтинг")

    class Meta:
        model = Review
        fields = ['course','name', 'email', 'rating', 'comment']
        labels = {
            'name': "Ім'я",
            'email': "Електронна пошта",
            'course': "Курс",
            'rating': "Оцінка",
            'comment': "Коментар"
        }