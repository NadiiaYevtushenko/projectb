from django.urls import path, include
from . import views
from .views import your_courses_view, course_detail_view
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .models import ConcreteProduct
from .views import sync_products_view


router = DefaultRouter()
router.register(r'products', views.ConcreteProductViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('courses1/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/videos/', views.course_videos_view, name='course_videos'),
    path('course/<int:course_id>/tests/', views.course_tests_view, name='course_tests'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('courses/<int:course_id>/demo_testing/', views.demo_testing_view, name='demo_testing'),
    path('your-courses/', your_courses_view, name='your_courses'),
    path('course/<int:course_id>/', course_detail_view, name='course_detail1'),
    path('api/', include(router.urls)),
    path('sync-products/', sync_products_view, name='sync_products'),
]