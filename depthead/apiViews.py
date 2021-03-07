from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course_List_All
from teacher.models import Course_Result_Theory


@csrf_exempt
def save_course(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    course = Course_List_All.objects.get(pk=id)
    if type == "course_code":
        course.course_code = value
    if type == "title":
        course.title = value
    if type == "credit":
        course.credit = value
    if type == "course_type":
        course.course_type = value
    course.save()
    return JsonResponse({"success": "updated"})


@csrf_exempt
def save_paper_code(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    course = Course_Result_Theory.objects.get(pk=id)
    if type == "Exam_Part_A_Code":
        course.Exam_Part_A_Code = value
    if type == "Exam_Part_B_Code":
        course.Exam_Part_B_Code = value
    course.save()
    return JsonResponse({"success": "updated"})
