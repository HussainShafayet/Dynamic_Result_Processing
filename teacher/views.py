from django.shortcuts import render,redirect
from accounts.models import Teacher
from .models import (Teachers, Course, Course_Result)
from django.contrib.auth.models import (User, auth, Group)
from django.contrib import messages
from depthead.models import batch_result
#from .forms import (Course_Result_Form)
from django.shortcuts import get_object_or_404
# Create your views here.


def teacher_dashboard(request):
    return render(request, 'user_dashboard.html')


def teacher_profile(request):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1+' '+v2
    assaigned_courses = Course.objects.filter(teacher=t_name)
    val= 'user_t'
    if assaigned_courses.exists() == False:
        messages.error(request, 'No Course Has Been Assaigned To You Yet')
    context = {
        'name': t_name,
        'course': assaigned_courses,
        'val': val
        
    }
    return render(request, 'teacher_Dashboard.html', context)


def course_result(request, Dy_id):
    x = Dy_id.find('+')
    batch = Dy_id[0:x]
    course = Dy_id[(x+1):]
    assigned_course = Course.objects.get(Batch=batch, Course=course)

    if (request.method == 'POST'):
        if('Calculate' in request.POST):
            gpa = 0.00
            grade = ''
            for i in assigned_course.course_result_set.all():
                total_marks = i.Term_test + i.Attendence + i.Exam_Part_A + i.Exam_Part_B
                if (total_marks < 40):
                    gpa = 0.00
                    grade = 'F'
                if (total_marks >= 40 and total_marks < 45):
                    gpa = 2.00
                    grade = 'C-'
                if (total_marks >= 45 and total_marks < 50):
                    gpa = 2.25
                    grade = 'C'
                if (total_marks >= 50 and total_marks < 55):
                    gpa = 2.50
                    grade = 'C+'
                if (total_marks >= 55 and total_marks < 60):
                    gpa = 2.75
                    grade = 'B-'
                if (total_marks >= 60 and total_marks < 65):
                    gpa = 3.00
                    grade = 'B'
                if (total_marks >= 65 and total_marks < 70):
                    gpa = 3.25
                    grade = 'B+'
                if (total_marks >= 70 and total_marks < 75):
                    gpa = 3.50
                    grade = 'A-'
                if (total_marks >= 75 and total_marks < 80):
                    gpa = 3.75
                    grade = 'A'
                if (total_marks >= 80):
                    gpa = 4.00
                    grade = 'A+'

                i.Total_mark = total_marks
                i.Grade_point = gpa
                i.Letter_grade = grade
                i.save()

        if('Submit' in request.POST):
            string_01 = ' GP'
            string_02 = ' LG'
            string_03 = course+string_01
            string_04 = course+string_02
            string_05 = string_03.replace(' ', '_')
            string_06 = string_04.replace(' ', '_')
            for i in assigned_course.course_result_set.all():
                reg = i.Reg_No
                GPA = i.Grade_point
                GRADE = i.Letter_grade
                batch_result_2 = batch_result.objects.get(Reg_No=reg)
                setattr(batch_result_2, string_05, GPA)
                setattr(batch_result_2, string_06, GRADE)
                batch_result_2.save()
    group = Group.objects.get(name='Teachers')
    return render(request, 'course_result.html', {'context': assigned_course, 'id': Dy_id, 'group': group})
""" def assignteacher(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    assign_teacher_list = AssignTeacher.objects.filter(teacher=teacher)
    val='assign_teacher'
    context = {
        'assign_teacher_list': assign_teacher_list,
        'val':val,
    }
    return render(request,'teacher.html',context) """

""" from django.views.generic import ListView
class Assignteacher(ListView):
    template_name = 'teacher.html'
    queryset = []
    def get_queryset(self,**kwargs):
        user2 = self.request.user
        teacher=get_object_or_404(Teacher,user=user2)
        return AssignTeacher.objects.filter(teacher=teacher) """
def course_result(request):
    if request.method == 'POST':
        form = Course_Result_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = Course_Result_Form()
        val = 'course_result'
        context = {
            'form': form,
            'val':val,
        }
        return render(request,'teacher.html',context)
