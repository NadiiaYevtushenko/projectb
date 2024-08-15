from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import contact_view, custom_logout_view, confirm_purchase, cancel_purchase

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('contact/', contact_view, name='contact'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('admin/purchase/confirm/<int:purchase_id>/', confirm_purchase, name='confirm_purchase'),
    path('admin/purchase/cancel/<int:purchase_id>/', cancel_purchase, name='cancel_purchase'),
]
