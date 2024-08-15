from django.shortcuts import render, get_object_or_404
from .models import Video
from courses.models import Course
from django.contrib.auth.decorators import login_required


@login_required
def course_videos(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.purchases.filter(course=course).exists():
        return render(request, 'video/access_denied.html')

    videos = Video.objects.filter(course=course).order_by('upload_date')
    return render(request, 'video/course_videos.html', {'course': course, 'videos': videos})
