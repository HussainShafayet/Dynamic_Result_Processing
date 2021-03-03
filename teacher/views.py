from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from accounts.models import Teacher
from .models import (Course, Course_Result_Theory,
                     Course_Result_Sessional, Teacher_name)
from django.contrib.auth.models import (User, auth, Group)
from django.contrib import messages
from depthead.models import (
    batch_result, Course_list, Sessions, Result_Table, Result_Semester_List)
from depthead.decorators import (login_required, allowed_user)
from student.models import Student_data
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required
@allowed_user(allowed_roles=['Teacher'])
def teacher_dashboard(request):
    return render(request, 'user_dashboard.html', {'val': 'user_t'})


@login_required
@allowed_user(allowed_roles=['Teacher'])
def assign_course(request):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1 + ' ' + v2
    teacher_obj = Teacher_name.objects.get(teacher=t_name)
    assaigned_courses = Course.objects.filter(teacher=teacher_obj)
    val = 'user_t'
    if assaigned_courses.exists() == False:
        messages.error(request, 'No Course Has Been Assaigned To You Yet')
    context = {
        'name': t_name,
        'course': assaigned_courses,
        'val': val,

    }
    return render(request, 'teacher_Dashboard.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
def assign_course_result(request):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1+' '+v2
    assaigned_courses = Course.objects.filter(teacher=t_name)
    if assaigned_courses.exists() == False:
        messages.error(request, 'No Course Has Been Assaigned To You Yet')
    context = {
        'name': t_name,
        'course': assaigned_courses,

    }
    return render(request, 'teacher_Dashboard.html', context)


def details_course(request, batch, course):
    course_details = Course.objects.get(Batch=batch, Course=course)
    course_details2 = Course_list.objects.get(course_code=course_details)
    val = 'course_det'
    context = {
        'course_details': course_details,
        'course_details2': course_details2,
        'val': val,
    }
    return render(request, 'teacher_Dashboard.html', context)


def course_result(request, batch, course):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        student_list = get_course.course_result_theory_set.all()
        val = 'course_result_theory'
        drop_student = Student_data.objects.all()
        context = {
            'student_list': student_list,
            'val': val,
            'batch': get_batch,
            'course': get_course,
            'drop_student': drop_student,
        }
        if request.method == 'POST':
            reg_no = request.POST.get('reg_no')
            if reg_no == 'null':
                messages.warning(request, 'Please select a registration no!')
                return redirect('course_result', batch, course)
            else:
                drop_student = Student_data.objects.get(Reg_No=reg_no)
                drop_session = drop_student.session
                get_name = drop_student.Name
                check_reg_no = Course_Result_Theory.objects.filter(
                    Reg_No=reg_no, batch=drop_session)
                if check_reg_no:
                    messages.warning(
                        request, 'This Registraion-No already exists!')
                    return redirect('course_result', batch, course)
                else:
                    add_drop = Course_Result_Theory(
                        course=get_course, batch=drop_session, Reg_No=reg_no, Name=get_name)
                    add_drop.save()
                    messages.success(request, 'Added successfully!')
                    return redirect('course_result', batch, course)
        return render(request, 'course_result_theory.html', context)
    elif course_type == 'Sessional':
        student_list = get_course.course_result_sessional_set.all()
        drop_student = Student_data.objects.all()
        val = 'course_result_sessional'
        context = {
            'student_list': student_list,
            'val': val,
            'batch': get_batch,
            'course': get_course,
            'drop_student': drop_student,
        }
        if request.method == 'POST':
            reg_no = request.POST.get('reg_no')
            if reg_no == 'null':
                messages.warning(request, 'Please select a registration no!')
                return redirect('course_result', batch, course)
            else:
                drop_student = Student_data.objects.get(Reg_No=reg_no)
                drop_session = drop_student.session
                get_name = drop_student.Name
                check_reg_no = Course_Result_Sessional.objects.filter(
                    Reg_No=reg_no, batch=drop_session)
                if check_reg_no:
                    messages.warning(
                        request, 'This Registraion-No already exists!')
                    return redirect('course_result', batch, course)
                else:
                    add_drop = Course_Result_Sessional(
                        course=get_course, batch=drop_session, Reg_No=reg_no, Name=get_name)
                    add_drop.save()
                    messages.success(request, 'Added successfully!')
                    return redirect('course_result', batch, course)
        return render(request, 'course_result_sessional.html', context)


def calculate_course_GPA(request, batch, course):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        gpa = 0.00
        grade = ''
        for i in get_course.course_result_theory_set.all():
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
    elif course_type == 'Sessional':
        gpa = 0.00
        grade = ''
        for i in get_course.course_result_sessional_set.all():
            total_marks = i.Attendence+i.Lab_performance + i.Exam
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

    return redirect('course_result', batch, course)


def result_submit(request, batch, course):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    course_semester = get_course.semester
    course_name = get_course.Course+' '+'LG'
    if course_type == 'Theory':
        string = get_batch.Batch+' '+course_semester
        get_list = Result_Table.objects.get(Reg=string)
        fieldlist = get_list.__dict__
        for field, value in fieldlist.items():
            LG_field = field
            if (course_name == value):
                break
            GP_field = LG_field

        student_list = get_course.course_result_theory_set.all()
        for i in student_list:
            Reg = i.Reg_No
            gp = i.Grade_point
            lg = i.Letter_grade
            sess = i.batch
            result_semester = Result_Semester_List.objects.get(
                Semester=course_semester, session=sess)
            find_student = Result_Table.objects.get(
                Reg=Reg, result_semester=result_semester)
            setattr(find_student, GP_field, gp)
            setattr(find_student, LG_field, lg)
            find_student.save()

    elif course_type == 'Sessional':
        string = get_batch.Batch+' '+course_semester
        get_list = Result_Table.objects.get(Reg=string)
        fieldlist = get_list.__dict__
        for field, value in fieldlist.items():
            LG_field = field
            if (course_name == value):
                break
            GP_field = LG_field

        student_list = get_course.course_result_sessional_set.all()
        for i in student_list:
            Reg = i.Reg_No
            gp = i.Grade_point
            lg = i.Letter_grade
            sess = i.batch
            result_semester = Result_Semester_List.objects.get(
                Semester=course_semester, session=sess)
            find_student = Result_Table.objects.get(
                Reg=Reg, result_semester=result_semester)
            setattr(find_student, GP_field, gp)
            setattr(find_student, LG_field, lg)
            find_student.save()

    return redirect('course_result', batch, course)


def delete_student(request, batch, course, id):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        del_std = Course_Result_Theory.objects.get(id=id).delete()
    elif course_type == 'Sessional':
        del_std = Course_Result_Sessional.objects.get(id=id).delete()
    return redirect('course_result', batch, course)


""" @login_required
@allowed_user(allowed_roles=['Teacher'])
def course_result(request, batch, course):
    #x = Dy_id.find('+')
    Dy_id = batch
    #batch = Dy_id[0:x]
    #course = Dy_id[(x+1):]
    assigned_course = Course.objects.get(Batch=batch, Course=course)

    if (request.method == 'POST'):
        if('Calculate' in request.POST):
            gpa = 0.00
            grade = ''
            for i in assigned_course.course_result_theory_set.all():
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
            for i in assigned_course.course_result_theory_set.all():
                reg = i.Reg_No
                GPA = i.Grade_point
                GRADE = i.Letter_grade
                batch_result_2 = batch_result.objects.get(Reg_No=reg)
                setattr(batch_result_2, string_05, GPA)
                setattr(batch_result_2, string_06, GRADE)
                batch_result_2.save()
    #group = Group.objects.get(name='Teacher')
    return render(request, 'course_result.html', {'context': assigned_course, 'id': Dy_id}) """


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
