from django.shortcuts import render
from depthead.models import Result_Table, Sessions, Result_Semester_List
from accounts.models import Student
from teacher.models import Course, Course_Result_Theory
from django.shortcuts import get_object_or_404
from depthead.decorators import (login_required, allowed_user)
# My views here.


@login_required
@allowed_user(allowed_roles=['Student'])
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


@login_required
@allowed_user(allowed_roles=['Student'])
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

    #Phase 1 - Column Names
    first_line = get_result[0]
    column_list = first_line.__dict__
    phase_1_start = ''
    X = 0
    for field, value in column_list.items():
        if value == 'Total Grade Point':
            skip_field = field
        if X == 1:
            phase_1_start = field
            break
        if value == 'Cumulative Grade':
            X = 1

    for field, value in column_list.items():
        temp = field
        if value is None:
            break
        phase_1_stop = temp

    my_list = []
    list_of_list = []
    start = 0
    my_list.append('Registration No')
    my_list.append('Name')

    for field, value in column_list.items():
        if field == phase_1_start:
            start = 1
        if start == 1:
            my_list.append(value)
        if field == phase_1_stop:
            break

    #Phase 2 - Column Names
    phase_2_start = ''
    Y = 0
    for field, value in column_list.items():
        if Y == 1:
            phase_2_start = field
            break
        if value == 'Name':
            Y = 1

    for field, value in column_list.items():
        if value == 'Cumulative Grade':
            break
        phase_2_stop = field

    start = 0
    for field, value in column_list.items():
        if field == skip_field:
            continue
        if field == phase_2_start:
            start = 1
        if start == 1:
            my_list.append(value)
        if field == phase_2_stop:
            break

    list_of_list.append(my_list)
    my_list = []

    #Phase 1 - Student
    my_list2 = []
    list_of_list_2 = []
    results = Result_Table.objects.filter(
        Reg=reg_no, batch=get_batch, result_semester=get_semester)
    for i in results:
        my_list2.append(i.Reg)
        my_list2.append(i.Name)
        column_list = i.__dict__
        start = 0
        for field, value in column_list.items():
            if field == phase_1_start:
                start = 1
            if start == 1:
                if value is None:
                    value = ' '
                my_list2.append(value)
            if field == phase_1_stop:
                break

        # Phase 2 - Students
        start = 0
        for field, value in column_list.items():
            if field == skip_field:
                continue
            if field == phase_2_start:
                start = 1
            if start == 1:
                if value is None:
                    value = ' '
                my_list2.append(value)
            if field == phase_2_stop:
                break

        list_of_list_2.append(my_list2)
        my_list2 = []

    list1 = []
    list_of_list1 = []

    for i in results:

        field_list = i._meta.get_fields()
        for j in field_list[3:]:
            val = getattr(i, j.name)
            if val == None:
                break
            else:
                list1.append(val)
        list_of_list1.append(list1)

    contex = {
        'results': list_of_list_2,
        'result2': list_of_list,
        'semester':get_semester,
    }
    return render(request, 'student.html', contex)
