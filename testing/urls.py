from django.urls import path
from . import views

app_name = 'testing'

urlpatterns = [
    path('course/<int:course_id>/tests/', views.course_tests_view, name='course_tests'),
    path('take_test/<int:course_id>/', views.take_test_view, name='take_test'),
    path('test/<int:test_id>/results/', views.test_results_view, name='test_results'),
]