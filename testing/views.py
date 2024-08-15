from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, Answer, StudentTestResult
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def course_tests_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tests = Test.objects.filter(course=course)
    return render(request, 'testing/course_tests.html', {'course': course, 'tests': tests})


@login_required
def take_test_view(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        score = 0
        total_questions = test.questions.count()
        for question in test.questions.all():
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
        final_score = (score / total_questions) * 100
        StudentTestResult.objects.create(student=request.user, test=test, score=final_score, passed=final_score >= 50)
        return redirect('test_results', test_id=test.id)
    else:
        return render(request, 'testing/take_test.html', {'test': test})


@login_required
def test_results_view(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    result = StudentTestResult.objects.get(student=request.user, test=test)
    return render(request, 'testing/test_results.html', {'result': result, 'test': test})
