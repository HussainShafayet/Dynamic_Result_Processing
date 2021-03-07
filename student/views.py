from django.shortcuts import render
from depthead.models import Result_Table, Sessions, Result_Semester_List
from accounts.models import Student
from teacher.models import Course, Course_Result_Theory
from django.shortcuts import get_object_or_404
from depthead.decorators import (login_required, allowed_user)
# My views here.


def student_dashboard(request):
    return render(request, 'user_dashboard.html', {'val': 'user_stud'})


@login_required
@allowed_user(allowed_roles=['Student'])
def active_courses(request):
    current_user = request.user
    student_obj = Student.objects.get(user=current_user)
    get_Reg = student_obj.reg_no
    batch = str(student_obj.batch)
    get_batch = Sessions.objects.get(Batch=batch)
    active_courses = Course.objects.filter(
        Batch=get_batch, Active=True, Course_type='Theory').order_by('Course')

    my_list = []
    list_of_list = []
    for courses in active_courses:
        get_obj = Course_Result_Theory.objects.get(
            Reg_No=get_Reg, course=courses)
        fieldlist = get_obj._meta.get_fields()
        course_obj = get_obj.course
        course = course_obj.Course
        my_list.append(course)
        
        for field in fieldlist[5:11]:
            value = getattr(get_obj, field.name)
            my_list.append(value)
        list_of_list.append(my_list)
        my_list = []
    
    val = 'active_courses'
    context = {
        'list_of_list': list_of_list,
        'val': val,
    }
    return render(request, 'student.html', context)


def student_result(request, semester):
    user2 = request.user
    stud = Student.objects.get(user=user2)
    reg_no = stud.reg_no
    session = stud.session
    batch = stud.batch
    get_batch = Sessions.objects.get(Batch=batch)
    get_semester = Result_Semester_List.objects.get(
        Semester=semester, session=get_batch)
    reg2 = str(batch)+' '+str(get_semester)
    get_result = Result_Table.objects.filter(
        Reg=reg2, result_semester=get_semester)

    course_list1 = []
    course_list_of_list1 = []
    course_list_of_list2 = []
    x = 0
    for i in get_result:
        field_list = i._meta.get_fields()

        for j in field_list[3:]:
            val = getattr(i, j.name)
            if val == None:
                break
            elif val == 'Name':
                x = 1
                course_list1.append(val)
            else:
                course_list1.append(val)
        if x == 1:
            course_list_of_list1.append(course_list1)
        else:
            course_list_of_list2.append(course_list1)
        course_list1 = []
        x = 2

    results = Result_Table.objects.filter(
        Reg=reg_no, batch=get_batch, result_semester=get_semester)
    list1 = []
    list_of_list1 = []
    list_of_list2 = []
    x = 0
    for i in results:

        field_list = i._meta.get_fields()
        for j in field_list[3:]:
            val = getattr(i, j.name)
            if val == None:
                break
            elif val == 'Name':
                x = 1
                list1.append(val)
            else:
                list1.append(val)
        if x == 1:
            list_of_list1.append(list1)
        else:
            list_of_list2.append(list1)
        list1 = []
        x = 2
    """ import operator
    sorted_list = sorted(list_of_list2, key=operator.itemgetter(0))
    for i in sorted_list:
        list_of_list1.append(i) """

    contex = {
        'results': list_of_list2,
        'result2': course_list_of_list1
    }
    return render(request, 'student.html', contex)
