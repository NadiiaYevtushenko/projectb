from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('<int:course_id>/', views.course_videos, name='course_videos'),
]
