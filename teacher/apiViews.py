from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course_Result_Theory



@csrf_exempt
def save_result(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    course = Course_Result_Theory.objects.get(id=id)
    if type == "Term_test":
        course.Term_test = value
    if type == "Attendence":
        course.Attendence = value
    if type == "Exam_Part_A":
        course.Exam_Part_A = value
    if type == "Exam_Part_B":
        course.Exam_Part_B = value
    course.save()
    return JsonResponse({"success":"updated"})
