from django.contrib import admin
from .models import Course, Video, Test


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'duration', 'price')
    search_fields = ('title', 'teacher__username', 'description')
    list_filter = ('teacher', 'price')


@admin.register(Video)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'question')
