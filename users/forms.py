from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_student', 'is_teacher')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ім'я")
    email = forms.EmailField(label="Електронна пошта")
    message = forms.CharField(widget=forms.Textarea, label="Ваш запит")