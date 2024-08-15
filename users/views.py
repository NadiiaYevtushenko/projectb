from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from courses.models import Course
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchaseConfirmation
from django.contrib.admin.views.decorators import staff_member_required

def register(request):
    """
    Реєстрація нового користувача.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """
    Відображає профіль користувача.
    """
    return render(request, 'users/profile.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Відправка електронного листа
            send_mail(
                f"Новий запит від {name}",
                message,
                email,  # Відправник
                ['your_email@example.com'],  # Замість цього вкажіть свій email для отримання повідомлень
                fail_silently=False,
            )

            return render(request, 'contact_success.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # або інша сторінка після входу
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    return render(request, 'users/logged_out.html')


@staff_member_required
def confirm_purchase(request, purchase_id):
    purchase = get_object_or_404(PurchaseConfirmation, id=purchase_id)
    purchase.is_confirmed = True
    purchase.save()
    return redirect('admin_purchase_list')  # Перенаправлення на список покупок, наприклад


@staff_member_required
def cancel_purchase(request, purchase_id):
    purchase = get_object_or_404(PurchaseConfirmation, id=purchase_id)
    purchase.is_confirmed = False
    purchase.save()
    return redirect('admin_purchase_list')


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    purchase = get_object_or_404(PurchaseConfirmation, course=course, student=request.user)

    if not purchase.is_confirmed:
        return render(request, 'courses/purchase_pending.html', {'course': course})

    return render(request, 'courses/course_detail.html', {'course': course})