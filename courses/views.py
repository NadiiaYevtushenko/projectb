from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Test, Video
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from .models import Course, DemoMaterial, Test
from users.models import PurchaseConfirmation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .models import ConcreteProduct
from .serializers import ConcreteProductSerializer
import requests
from django.http import HttpResponse
from .sync import sync_products_from_project_a
from .tasks import send_notification_email


def some_view(request):
    # Виклик асинхронної задачі
    send_notification_email.delay('Subject', 'Message', ['recipient@example.com'])
    return HttpResponse("Email sent!")


def sync_products_view(request):
    sync_products_from_project_a()
    return HttpResponse("Синхронізація завершена!")


class ConcreteProductViewSet(viewsets.ModelViewSet):
    queryset = ConcreteProduct.objects.all()
    serializer_class = ConcreteProductSerializer


def home(request):
    """
    Головна сторінка, де відображаються всі курси.
    """
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def course_list(request):
    """
    Відображає список всіх курсів.
    """
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, pk):
    """
    Відображає детальну інформацію про курс, включаючи доступні відеоуроки та тести.
    """
    course = get_object_or_404(Course, pk=pk)
    lessons = Video.objects.filter(course=course)
    tests = Test.objects.filter(course=course)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'tests': tests,
    })


@login_required
def course_videos_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = Video.objects.filter(course=course)  # Отримання відео для конкретного курсу
    return render(request, 'courses/course_video.html', {'course': course, 'videos': videos})


@login_required
def course_tests_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tests = Test.objects.filter(course=course)  # Отримання тестів для конкретного курсу
    return render(request, 'course_tests.html', {'course': course, 'tests': tests})


def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    context = {
        'reviews': reviews,
        'form': form
    }
    return render(request, 'reviews.html', context)


def demo_testing_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    demo_materials = DemoMaterial.objects.filter(course=course)
    tests = Test.objects.filter(course=course)
    return render(request, 'courses/demo_testing.html', {
        'course': course,
        'demo_materials': demo_materials,
        'tests': tests
    })


def your_courses_view(request):
    # Отримання підтверджених покупок для поточного користувача
    confirmed_purchases = PurchaseConfirmation.objects.filter(student=request.user, is_confirmed=True)

    # Отримання курсів з підтверджених покупок
    courses = [purchase.course for purchase in confirmed_purchases]

    context = {
        'courses': courses
    }
    return render(request, 'users/your_courses.html', context)


def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    context = {
        'course': course,
    }
    return render(request, 'courses/course_detail1.html', context)