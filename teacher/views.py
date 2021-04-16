from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from accounts.models import Teacher
from .models import (Course,
                     Course_Result_Sessional, Teacher_name, Course_Khata, Course_Result_Theory)
from django.contrib.auth.models import (User, auth, Group)
from django.contrib import messages
from depthead.models import (
      Sessions, Result_Table, Result_Semester_List)
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
    assaigned_courses = Course.objects.filter(teacher=teacher_obj, Active=True)
    val = 'user_t'
    context = {
        'name': t_name,
        'course': assaigned_courses,
        'val': val,

    }
    return render(request, 'teacher_Dashboard.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
def completed_courses(request):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1 + ' ' + v2
    teacher_obj = Teacher_name.objects.get(teacher=t_name)
    assaigned_courses = Course.objects.filter(
        teacher=teacher_obj, Active=False)
    val = 'user_t2'
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
    context = {
        'name': t_name,
        'course': assaigned_courses,

    }
    return render(request, 'teacher_Dashboard.html', context)


""" @login_required
@allowed_user(allowed_roles=['Teacher'])
def details_course(request, batch, course):
    course_details = Course.objects.get(Batch=batch, Course=course)
    course_details2 = Course_list.objects.get(course_code=course_details)
    val = 'course_det'
    context = {
        'course_details': course_details,
        'course_details2': course_details2,
        'val': val,
    }
    return render(request, 'teacher_Dashboard.html', context) """


@login_required
@allowed_user(allowed_roles=['Teacher'])
def course_result(request, batch, course):
    current_user = request.user
    teacher = Teacher.objects.get(user=current_user)
    dept = teacher.dept
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        student_list = get_course.course_result_theory_set.all()
        val = 'course_result_theory'
        drop_student = Student_data.objects.filter(dept=dept)
        context = {
            'student_list': student_list,
            'val': val,
            'batch': get_batch,
            'course': get_course,
            'drop_student': drop_student,
        }
        if request.method == 'POST':
            if 'drop_student' in request.POST:
                reg_no = request.POST.get('reg_no')
                drop_semester = request.POST.get('select_semester')
                if reg_no is None:
                    messages.warning(
                        request, 'Please select a registration no!')
                    return redirect('course_result', batch, course)
                else:
                    drop_student = Student_data.objects.get(Reg_No=reg_no)
                    drop_session = drop_student.session
                    get_name = drop_student.Name
                    check_reg_no = get_course.course_result_theory_set.filter(
                        Reg_No=reg_no)
                    if not check_reg_no:
                        add_drop = Course_Result_Theory(
                            course=get_course, batch=drop_session, Reg_No=reg_no, Name=get_name, semester=drop_semester)
                        add_drop.save()
                        messages.success(request, 'Added successfully!')
                        return redirect('course_result', batch, course)
                    else:
                        messages.warning(
                            request, 'This Registraion. No. already exists!')
                        return redirect('course_result', batch, course)
            if 'calculate' in request.POST:

                Count_TT = request.POST['count_TT']
                TT_Count = int(Count_TT)
                get_marks = 0
                myList = []
                studentList = get_course.course_result_theory_set.all().order_by('Reg_No')
                for i in studentList:
                    myList.append(i.Term_Test_01)
                    myList.append(i.Term_Test_02)
                    myList.append(i.Term_Test_03)
                    myList.sort(reverse=True)
                    selected_List = myList[:TT_Count]
                    for j in selected_List:
                        get_marks += j

                    mark_actual = get_marks/TT_Count
                    mark_rounded = round(mark_actual)
                    total_mark = i.Attendence+mark_rounded
                    setattr(i, 'Term_Test_Total', mark_rounded)
                    setattr(i, 'Pre_Final_Total', total_mark)
                    i.save()
                    myList = []
                    get_marks = 0
                return redirect('course_result', batch, course)
            if 'change_state' in request.POST:
                get_course.Active = False
                get_course.save()
                return redirect('assign_course')
        return render(request, 'course_result_theory.html', context)
    elif course_type == 'Sessional':
        student_list = get_course.course_result_sessional_set.all()
        drop_student = Student_data.objects.filter(dept=dept)
        val = 'course_result_sessional'
        context = {
            'student_list': student_list,
            'val': val,
            'batch': get_batch,
            'course': get_course,
            'drop_student': drop_student,
        }
        if request.method == 'POST':
            if 'drop_student_sessional' in request.POST:
                reg_no = request.POST.get('reg_no')
                drop_semester_sessional = request.POST.get('select_semester')
                if reg_no is None:
                    messages.warning(
                        request, 'Please select a registration no!')
                    return redirect('course_result', batch, course)
                else:
                    drop_student = Student_data.objects.get(Reg_No=reg_no)
                    drop_session = drop_student.session
                    get_name = drop_student.Name
                    check_reg_no = get_course.course_result_sessional_set.filter(
                        Reg_No=reg_no)
                    if not check_reg_no:
                        add_drop = Course_Result_Sessional(
                            course=get_course, batch=drop_session, Reg_No=reg_no, Name=get_name, semester=drop_semester_sessional)
                        add_drop.save()
                        messages.success(request, 'Added successfully!')
                        return redirect('course_result', batch, course)
                    else:
                        messages.warning(
                            request, 'This Registraion. No. already exists!')
                        return redirect('course_result', batch, course)
            if 'calculate_sessional' in request.POST:
                studentList = get_course.course_result_sessional_set.all().order_by('Reg_No')
                for i in studentList:
                    total_marks = i.Attendence + i.Lab_performance + i.Exam
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
            if 'submit_sessional' in request.POST:
                get_batch = Sessions.objects.get(Batch=batch)
                get_course = Course.objects.get(Course=course, Batch=get_batch)

                course_semester = get_course.semester
                course_name = get_course.Course+' LG'
                string = get_batch.Batch+' '+course_semester
                get_list = Result_Table.objects.get(Reg=string)
                fieldlist = get_list.__dict__
                for field, value in fieldlist.items():
                    LG_field = field
                    if (course_name == value):
                        break
                    GP_field = LG_field

                student_list = get_course.course_result_sessional_set.filter(
                    semester=course_semester)

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

                drop_student_list = get_course.course_result_sessional_set.all().exclude(
                    semester=course_semester)
                for i in drop_student_list:
                    session_obj = i.batch
                    semester = i.semester
                    gp = i.Grade_point
                    lg = i.Letter_grade
                    registration = i.Reg_No
                    find_semester = Result_Semester_List.objects.get(
                        session=session_obj, Semester=semester)
                    get_course = Course.objects.get(
                        Course=course, Batch=get_batch)
                    course_name = get_course.Course+' LG'

                    all_students = find_semester.result_table_set.filter(
                        Name='Name')
                    first_line = all_students[0]
                    fieldlist = first_line.__dict__
                    for field, value in fieldlist.items():
                        LG_field = field
                        if (course_name == value):
                            break
                        GP_field = LG_field

                    find_student = Result_Table.objects.get(
                        Reg=registration, result_semester=find_semester)
                    setattr(find_student, GP_field, gp)
                    setattr(find_student, LG_field, lg)
                    find_student.save()

                get_course.Active = False
                get_course.save()
                return redirect('assign_course')
        return render(request, 'course_result_sessional.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
def archived_course(request, batch, course):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(
        Course=course, Batch=get_batch,)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        student_list = get_course.course_result_theory_set.all()
        val = 'theory'
        context = {
            'student_list': student_list,
            'course': get_course,
            'val': val,
        }

        return render(request, 'archive_courses.html', context)
    elif course_type == 'Sessional':
        student_list = get_course.course_result_sessional_set.all()
        val = 'sessional'
        context = {
            'student_list': student_list,
            'course': get_course,
            'val': val,
        }
        return render(request, 'archive_courses.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
def exam_khata(request):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1 + ' ' + v2
    teacher_obj = Teacher_name.objects.get(teacher=t_name)
    assaigned_courses = Course_Khata.objects.filter(
        teacher=teacher_obj, Active=True)
    val = 'exam_khata'
    context = {
        'courses': assaigned_courses,
        'val': val,
    }

    return render(request, 'exam_khata.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
def assaigned_khatas(request, batch, course):
    current_user = request.user
    v1 = current_user.first_name
    v2 = current_user.last_name
    t_name = v1 + ' ' + v2
    teacher_obj = Teacher_name.objects.get(teacher=t_name)
    get_batch = Sessions.objects.get(Batch=batch)
    get_course_object = Course.objects.get(Batch=get_batch, Course=course)
    get_khata_object = Course_Khata.objects.get(
        batch=get_batch, Course_Code=course, teacher=teacher_obj)
    part = get_khata_object.Exam_Part
    if part == 'Part A':
        student_list = get_course_object.course_result_theory_set.all().order_by(
            'Exam_Part_A_Code')
    else:
        student_list = get_course_object.course_result_theory_set.all().order_by(
            'Exam_Part_B_Code')
    val = 'exam_khata_detail'
    context = {
        'student_list': student_list,
        'part': part,
        'batch': batch,
        'course': course,
    }
    if request.method == 'POST':
        get_khata_object.Active = False
        get_khata_object.save()
        return redirect('exam_khata')
    return render(request, 'exam_khata.html', context)


@login_required
@allowed_user(allowed_roles=['Teacher'])
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


@login_required
@allowed_user(allowed_roles=['Teacher'])
def delete_student(request, batch, course, id):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Course=course, Batch=get_batch)
    course_type = get_course.Course_type
    if course_type == 'Theory':
        del_std = Course_Result_Theory.objects.get(id=id).delete()
    elif course_type == 'Sessional':
        del_std = Course_Result_Sessional.objects.get(id=id).delete()
    return redirect('course_result', batch, course)
