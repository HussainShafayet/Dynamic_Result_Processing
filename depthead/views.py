from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import (User, Group,)
from accounts.models import (Student, Teacher, Depthead)
from django.contrib.auth import get_user_model
from .forms import (AddCourse, Create_batch, AddSyllabus, Add_Semester)
from .models import (Course_list, Batch, Session,
                     Student_Sessions, batch_result, Dept, Syllabus, Course_Semester_List, Sessions, Result_Semester_List, Result_Table, Course_List_All)
from teacher.models import (Course,
                            Course_Result_Sessional, Teacher_name, Course_Result_Theory, Course_Khata)
from student.models import(Student_data)
from django.contrib import messages
from .decorators import login_required, allowed_user
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response
# pdf
from django.template.loader import get_template
from django.http import HttpResponse
import pdfkit
import os
import shutil
from PyPDF2 import PdfFileMerger


# Create your views here.
@login_required
@allowed_user(allowed_roles=['DeptHead'])
def depthead_home(request):
    return render(request, 'user_Dashboard.html', {'val': 'user_dh', })

# Users,Userdetails and Allowuser


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def users(request):
    if 'search' in request.GET:
        q = request.GET.get('search')
        if q:
            group = Group.objects.get(name='None')
            User = get_user_model()
            user_list = User.objects.filter(groups=group).filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=str(q)) | Q(username__icontains=q) | Q(email__icontains=str(q)))
            if user_list:
                val = 'user_val'
                context = {
                    'user_list': user_list,
                    'val': val,
                }
                return render(request, 'users.html', context)
            else:
                messages.warning(request, 'No result found')
                val = 'user_val'
                context = {
                    'val': val,
                }
                return render(request, 'users.html', context)
        else:
            current_user = request.user
            dept_head = Depthead.objects.get(user=current_user)
            dept = dept_head.dept
            teacher_list = Teacher.objects.filter(dept=dept)
            student_list = Student.objects.filter(dept=dept)

            user_list2 = []
            for i in teacher_list:
                user_obj = i.user
                user_list2.append(user_obj)

            for i in student_list:
                user_obj = i.user
                user_list2.append(user_obj)
            user_list = []
            for i in user_list2:
                if i.is_student is False and i.is_teacher is False:
                    user_list.append(i)
            val = 'user_val'
            context = {
                'user_list': user_list,
                'val': val,
            }
            return render(request, 'users.html', context)

    else:
        current_user = request.user
        dept_head = Depthead.objects.get(user=current_user)
        dept = dept_head.dept
        teacher_list = Teacher.objects.filter(dept=dept)
        student_list = Student.objects.filter(dept=dept)

        user_list2 = []
        for i in teacher_list:
            user_obj = i.user
            user_list2.append(user_obj)

        for i in student_list:
            user_obj = i.user
            user_list2.append(user_obj)
        user_list = []
        for i in user_list2:
            if i.is_student is False and i.is_teacher is False:
                user_list.append(i)

        val = 'user_val'
        context = {
            'user_list': user_list,
            'val': val,
        }
        return render(request, 'users.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def search(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        User = get_user_model()
        user_list = User.objects.filter(groups__name='None').filter(
            Q(first_name__icontains=search_str) | Q(last_name__icontains=str(search_str)) | Q(username__icontains=str(search_str)) | Q(email__icontains=str(search_str)))
        data = user_list.values()
        return JsonResponse(list(data), safe=False)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def userdetails(request, id):
    user = request.user
    User = get_user_model()
    user_det = User.objects.get(id=id)
    group = Group.objects.get(user=user_det)
    val = 'userdetails'
    context = {
        'user': user,
        'user_det': user_det,
        'group': group,
        'val': val
    }
    return render(request, 'users.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def allow_user(request, id):
    User = get_user_model()
    user_det = User.objects.get(id=id)
    if request.POST.get('group'):
        grop_name = request.POST.get('group')
        if grop_name == 'Teacher':
            group = Group.objects.get(name='Teacher')
            user_det.groups.add(group)
            g = Group.objects.get(name='None')
            user_det.groups.remove(g)
            user_det.is_teacher = True
            user_det.save()
            n1 = user_det.first_name
            n2 = user_det.last_name
            name = n1 + ' ' + n2
            add_teacher_name = Teacher_name(teacher=name)
            add_teacher_name.save()
            return redirect('users')
        elif grop_name == 'Student':
            group = Group.objects.get(name='Student')
            user_det.groups.add(group)
            g = Group.objects.get(name='None')
            user_det.groups.remove(g)
            user_det.is_none = False
            user_det.is_student = True
            user_det.save()
            n1 = user_det.first_name
            n2 = user_det.last_name
            name = n1 + ' ' + n2
            stud = Student.objects.get(user=user_det)
            reg = stud.reg_no
            batch = stud.batch
            dept = stud.dept
            get_sess = Sessions.objects.get(Batch=batch)
            add_student = Student_data(
                session=get_sess, Reg_No=reg, Name=name, dept=str(dept))
            add_student.save()
            semester_list = Result_Semester_List.objects.filter(
                session=get_sess)
            for i in semester_list:
                New_student = Result_Table(
                    Reg=reg, Name=name, result_semester=i, batch=get_sess)
                New_student.save()
            return redirect('users')
    else:
        user_det = User.objects.get(id=id)
    context = {
        'user_det': user_det,
        'val': 'user_details'
    }
    return render(request, 'users.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def delete_user(request, id):
    User = get_user_model()
    user_del = User.objects.get(id=id)
    user_del.delete()
    return redirect('users')


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def student_info(request):
    if 'search' in request.GET:
        q = request.GET.get('search')
        if q:
            current_user = request.user
            dept_head = Depthead.objects.get(user=current_user)
            dept = dept_head.dept
            student_list = Student.objects.filter(dept=dept)
            stud_info = []
            for i in student_list:
                user_obj = i.user
                if user_obj.is_student == True:
                    stud_info.append(user_obj)
            query = Q()
            for item in stud_info:
                query |= (Q(username=item.username))

            User = get_user_model()
            stud_info2 = User.objects.filter(query).filter(
                Q(first_name__icontains=str(q)) | Q(last_name__icontains=str(q)) | Q(username__icontains=str(q)) | Q(email__icontains=str(q)))

            if stud_info2:
                val = 'std_info'
                context = {
                    'stud_info': stud_info2,
                    'val': val,
                }
                return render(request, 'users.html', context)
            else:
                messages.error(request, 'No result found')
                val = 'std_info'
                context = {
                    'val': val,
                }
                return render(request, 'users.html', context)
        else:
            current_user = request.user
            dept_head = Depthead.objects.get(user=current_user)
            dept = dept_head.dept
            student_list = Student.objects.filter(dept=dept)
            stud_info = []
            for i in student_list:
                user_obj = i.user
                if user_obj.is_student == True:
                    stud_info.append(user_obj)
            val = 'std_info'
            context = {
                'stud_info': stud_info,
                'val': val,
            }
            return render(request, 'users.html', context)
    else:
        current_user = request.user
        dept_head = Depthead.objects.get(user=current_user)
        dept = dept_head.dept
        student_list = Student.objects.filter(dept=dept)
        stud_info = []
        for i in student_list:
            user_obj = i.user
            if user_obj.is_student == True:
                stud_info.append(user_obj)
        val = 'std_info'
        context = {
            'stud_info': stud_info,
            'val': val,
        }
        return render(request, 'users.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def student_search(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        current_user = request.user
        dept_head = Depthead.objects.get(user=current_user)
        dept = dept_head.dept
        student_list = Student.objects.filter(dept=dept)
        stud_info = []
        for i in student_list:
            user_obj = i.user
            if user_obj.is_student == True:
                stud_info.append(user_obj)
        query = Q()
        for item in stud_info:
            query |= (Q(username=item.username))
        """ query2 = Q()
        for j in student_list:
            query2 |= (Q(user=j.user))
        test = Student.objects.filter(query2).filter(
            reg_no__icontains=search_str)
        print(test)
        print(type(test)) """
        User = get_user_model()
        stud_info2 = User.objects.filter(query).filter(
            Q(first_name__icontains=str(search_str)) | Q(last_name__icontains=str(search_str)) | Q(username__icontains=str(search_str)) | Q(email__icontains=str(search_str)))
        # print(type(stud_info2))
        #from itertools import chain
        #stud_info3 = chain(test, stud_info2)
        # print(stud_info3)
        data = stud_info2.values()

        for i in data:
            foreign_key = i['id']
            use_obj = User.objects.get(pk=int(foreign_key))
            stu_obj = Student.objects.get(user=use_obj)
            mydict = {}
            column_list = stu_obj._meta.get_fields()
            for column in column_list[1:7]:
                value = getattr(stu_obj, column.name)
                #print(column.name, value)
                mydict[column.name] = str(value)
            # print(mydict)
            i['related_values'] = mydict
        # print(data)
        return JsonResponse(list(data), safe=False)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def teacher_info(request):
    if 'search' in request.GET:
        q = request.GET.get('search')
        if q:
            current_user = request.user
            dept_head = Depthead.objects.get(user=current_user)
            dept = dept_head.dept
            teacher_list = Teacher.objects.filter(dept=dept)
            teach_info = []
            for i in teacher_list:
                user_obj = i.user
                if user_obj.is_teacher == True:
                    teach_info.append(user_obj)
            query = Q()
            for item in teach_info:
                query |= (Q(username=item.username))

            User = get_user_model()
            teacher_info = User.objects.filter(query).filter(Q(first_name__icontains=str(q)) | Q(
                last_name__icontains=str(q)) | Q(username__icontains=str(q)) | Q(email__icontains=str(q)))
            if teacher_info:
                val = 'teach_info'
                context = {
                    'teacher_info': teacher_info,
                    'val': val,
                }
                return render(request, 'users.html', context)
            else:
                messages.error(request, 'No result found')
                val = 'teach_info'
                context = {
                    'val': val,
                }
                return render(request, 'users.html', context)
        else:
            current_user = request.user
            dept_head = Depthead.objects.get(user=current_user)
            dept = dept_head.dept
            teacher_list = Teacher.objects.filter(dept=dept)
            teacher_info = []
            for i in teacher_list:
                user_obj = i.user
                if user_obj.is_teacher == True:
                    teacher_info.append(user_obj)
            val = 'teach_info'
            context = {
                'teacher_info': teacher_info,
                'val': val,
            }
            return render(request, 'users.html', context)
    else:
        current_user = request.user
        dept_head = Depthead.objects.get(user=current_user)
        dept = dept_head.dept
        teacher_list = Teacher.objects.filter(dept=dept)
        teacher_info = []
        for i in teacher_list:
            user_obj = i.user
            if user_obj.is_teacher == True:
                teacher_info.append(user_obj)
        val = 'teach_info'
        context = {
            'teacher_info': teacher_info,
            'val': val,
        }
        return render(request, 'users.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def teacher_search(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        current_user = request.user
        dept_head = Depthead.objects.get(user=current_user)
        dept = dept_head.dept
        teacher_list = Teacher.objects.filter(dept=dept)
        teach_info = []
        for i in teacher_list:
            user_obj = i.user
            if user_obj.is_teacher == True:
                teach_info.append(user_obj)
        query = Q()
        for item in teach_info:
            query |= (Q(username=item.username))

        User = get_user_model()
        teacher_info = User.objects.filter(query).filter(
            Q(first_name__icontains=str(search_str)) | Q(last_name__icontains=str(search_str)) | Q(username__icontains=str(search_str)) | Q(email__icontains=str(search_str)))
        data = teacher_info.values()
        for i in data:
            foreign_key = i['id']
            use_obj = User.objects.get(pk=int(foreign_key))
            teach_obj = Teacher.objects.get(user=use_obj)
            mydict = {}
            column_list = teach_obj._meta.get_fields()
            for column in column_list[1:]:
                value = getattr(teach_obj, column.name)
                mydict[column.name] = str(value)
            i['related_values'] = mydict
        return JsonResponse(list(data), safe=False)


# add Syllabus and view syllabus
@login_required
@allowed_user(allowed_roles=['DeptHead'])
def add_syllabus(request):
    if request.method == 'POST':
        form = AddSyllabus(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            syllabus = form.cleaned_data['Syllabus_Name']
            get_syl = Syllabus.objects.get(Syllabus_Name=syllabus)
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='1st')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='2nd')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='3rd')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='4th')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='5th')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='6th')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='7th')
            new_semester.save()
            new_semester = Course_Semester_List(
                syllabus=get_syl, Semester='8th')
            new_semester.save()
            messages.success(request, 'Add successfully!')
            return redirect('syllabus')
        else:
            messages.warning(request, 'Try again!')
            val1 = 'add_syllabus'
            context = {
                'form': form,
                'val1': val1,
            }
        return render(request, 'syllabus.html', context)
    else:
        form = AddSyllabus(user=request.user)
        val1 = 'add_syllabus'
        val2 = 'syllabus_semester'
        context = {
            'form': form,
            'val1': val1,
            'val2': val2,
        }
        return render(request, 'syllabus.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def view_syllabus(request):
    depthead = Depthead.objects.get(user=request.user)
    dept = depthead.dept
    syllabus = Syllabus.objects.filter(dept=dept).order_by('Syllabus_Name')
    val = 'view_syllabus'
    context = {
        'syllabus': syllabus,
        'val': val,
    }
    return render(request, 'syllabus.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def syllabus_semester(request, syllabus_id):
    syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
    semester = Course_Semester_List.objects.filter(syllabus=syllabus)
    syllabus_id = syllabus_id
    val2 = 'syllabus_semester'
    context = {
        'semester': semester,
        'val2': val2,
        'syllabus_id': syllabus_id,
    }
    return render(request, 'syllabus.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def add_course(request, syllabus_id, semester):
    if request.method == 'POST':
        form = AddCourse(request.POST)
        if form.is_valid():
            syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
            dept = syllabus.dept
            semester = Course_Semester_List.objects.get(
                Semester=semester, syllabus=syllabus)
            course_code = form.cleaned_data['course_code']
            title = form.cleaned_data['title']
            credit = form.cleaned_data['credit']
            course_type = form.cleaned_data['course_type']
            get_course = Course_List_All.objects.filter(
                semester=semester, course_code=course_code)
            if get_course:
                messages.warning(request, 'This course already exists!')
                context = {
                    'form': form,
                }
                return render(request, 'course_list.html', context)
            else:
                Add_course = Course_List_All(
                    dept=dept, semester=semester, course_code=course_code, title=title, credit=credit, course_type=course_type)
                Add_course.save()
                messages.success(request, 'Courses added successfully!')
                return redirect('view_course_list', syllabus_id, semester)
        else:
            messages.warning(request, 'Try again!')
            context = {
                'form': form,
            }
        return render(request, 'course_list.html', context)
    else:
        form = AddCourse()
        context = {
            'form': form,
        }
        return render(request, 'course_list.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def view_course_list_all(request, syllabus_id, semester):
    syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
    search_syllabus = Sessions.objects.filter(syllabus=syllabus)
    semester_list = Course_Semester_List.objects.filter(syllabus=syllabus)
    if search_syllabus:
        value = 'hide'
    else:
        value = 'visible'
    get_semester = Course_Semester_List.objects.get(
        syllabus=syllabus, Semester=semester)

    course_list = get_semester.course_list_all_set.all()
    val = 'course_list_by_semester'
    context = {
        'course_list': course_list,
        'val': val,
        'semester': semester,
        'syllabus_id': syllabus_id,
        'value': value,
        'semester_list': semester_list,
    }
    return render(request, 'course_list.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def delete_course(request, syllabus_id, semester, id):
    del_course = Course_List_All.objects.get(pk=id).delete()
    messages.success(request, 'This course is deleted succesfully!!!')
    return redirect('view_course_list', syllabus_id, semester)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def create_batch(request):
    if request.method == 'POST':
        form = Create_batch(request.POST, user=request.user)
        if form.is_valid():
            depthead = Depthead.objects.get(user=request.user)
            dept = depthead.dept
            syllabus = form.cleaned_data['syllabus']
            batch = form.cleaned_data['Batch']
            session = form.cleaned_data['Session']
            new_batch = Batch(batch=batch)
            new_batch.save()
            new_session = Session(session=session)
            new_session.save()
            syllabus = Syllabus.objects.get(Syllabus_Name=syllabus)
            New_session = Sessions(
                dept=dept, syllabus=syllabus, Batch=batch, Session=session)
            New_session.save()

            get_semesters = syllabus.course_semester_list_set.all()
            get_session = Sessions.objects.get(Batch=batch, Session=session)
            for i in get_semesters:
                add_semesters = Result_Semester_List(
                    Semester=i.Semester, session=get_session)
                add_semesters.save()

            result_semesters = get_session.result_semester_list_set.all()
            for i in result_semesters:
                string_01 = i.Semester
                string_02 = batch
                string_03 = string_02 + " " + string_01
                string_Name = "Name"
                add_data = Result_Table(
                    result_semester=i, Reg=string_03, Name=string_Name, batch=get_session)
                add_data.save()

                syllabus_semesters = syllabus.course_semester_list_set.all()
                get_Sem = syllabus_semesters.get(Semester=i.Semester)
                courses_01 = get_Sem.course_list_all_set.all()
                courses_02 = []
                for k in courses_01:
                    string_04 = k.course_code+" GP"
                    courses_02.append(string_04)
                    string_05 = k.course_code+" LG"
                    courses_02.append(string_05)
                courses_02.append("Credit")
                courses_02.append("Total Grade Point")
                courses_02.append("Grade Point")
                courses_02.append("Grade")
                courses_02.append('Total Credit')
                courses_02.append('Cumulative Grade Point')
                courses_02.append('Cumulative Grade')

                for j in i.result_table_set.all():
                    fieldList1 = j._meta.get_fields()
                    fieldList2 = fieldList1[5:]
                    Two_list = zip(fieldList2, courses_02)
                    for l, m in Two_list:
                        string_06 = l.name
                        string_07 = m
                        setattr(j, string_06, string_07)
                        j.save()

            return redirect('find_batch')
        else:
            messages.warning(request, 'Try again!')
            context = {
                'form': form,
            }
            return render(request, 'create_batch.html', context)
    else:
        form = Create_batch(user=request.user)
        context = {
            'form': form,
        }
        return render(request, 'create_batch.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def find_batch(request):
    depthead = Depthead.objects.get(user=request.user)
    dept = depthead.dept
    batches = Sessions.objects.filter(dept=dept).order_by('Session')
    val = 'batch_info'
    context = {
        'batches': batches,
        'val': val,
    }
    return render(request, 'batch_info.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def batch_info(request, batch):
    batch2 = Sessions.objects.get(Batch=batch)
    semester_list = Result_Semester_List.objects.filter(session=batch2)
    # result_semester_list = batch.result_semester_list_set.all()
    val2 = 'sidelink'
    context = {
        'result_semester_list': semester_list,
        'val': 'result_semester_list_info',
        'batch_val': batch,
        'val2': val2,

    }
    return render(request, 'batch_info.html', context)


def calculate_GPA(batch, semester):
    get_batch = Sessions.objects.get(Batch=batch)
    get_syllabus = get_batch.syllabus
    semester_string = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester)
    get_x = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester_string)
    #course_list = get_x.course_list_all_set.all()
    get_semester = Result_Semester_List.objects.get(
        session=get_batch, Semester=semester)

    drop_courses_list = []
    course_semesters = get_syllabus.course_semester_list_set.all()
    for i in course_semesters:
        for j in i.course_list_all_set.all():
            drop_courses_list.append(j)

    my_dict = {}
    for i in drop_courses_list:
        my_dict[i.course_code] = i.credit

    search_string = get_batch.Batch + ' ' + semester_string.Semester
    find_obj = Result_Table.objects.get(Reg=search_string)
    column_list = find_obj.__dict__
    for field, value in column_list.items():
        if value == 'Credit':
            credit = field
        if value == 'Total Grade Point':
            total_point = field
        if value == 'Grade Point':
            point = field
        if value == 'Grade':
            grade = field
        if value == 'Total Credit':
            CGPA_credit = field
        if value == 'Cumulative Grade Point':
            CGPA = field
        if value == 'Cumulative Grade':
            CGPA_grade = field

    student_list2 = get_semester.result_table_set.all().exclude(Reg=search_string)
    for student in student_list2:
        credit_count = 0
        gpa_count = 0
        fieldlist = student.__dict__
        for field, value in fieldlist.items():
            if (value is None):
                continue
            course_name = getattr(find_obj, field)
            course_string = str(course_name)

            if 'GP' in course_string:
                course_gpa2 = value
                course_gpa = float(course_gpa2)
                course_code = course_string[:-3]
                find_credit = my_dict[course_code]
                if(course_gpa < 2.00):
                    continue
                if(course_gpa >= 2.00):
                    gpa_count += course_gpa*find_credit
                    credit_count += find_credit

        if (credit_count == 0):
            GPA_full = 0.00
        else:
            GPA_full = gpa_count / credit_count

        GPA = round(GPA_full, 2)

        if(GPA < 2.00):
            letter_grade = 'F'
        if(GPA >= 2.00 and GPA < 2.25):
            letter_grade = 'C-'
        if(GPA >= 2.25 and GPA < 2.50):
            letter_grade = 'C'
        if(GPA >= 2.50 and GPA < 2.75):
            letter_grade = 'C+'
        if(GPA >= 2.75 and GPA < 3.00):
            letter_grade = 'B-'
        if(GPA >= 3.00 and GPA < 3.25):
            letter_grade = 'B'
        if(GPA >= 3.25 and GPA < 3.50):
            letter_grade = 'B+'
        if(GPA >= 3.50 and GPA < 3.75):
            letter_grade = 'A-'
        if(GPA >= 3.75 and GPA < 4.00):
            letter_grade = 'A'
        if(GPA == 4.00):
            letter_grade = 'A+'

        setattr(student, credit, credit_count)
        setattr(student, total_point, gpa_count)
        setattr(student, point, GPA)
        setattr(student, grade, letter_grade)
        student.save()
        GPA = 0
        letter_grade = ' '

    # Calculate CGPA
    result_semesters = []
    result_semesters_2 = get_batch.result_semester_list_set.all().order_by('Semester')
    for i in result_semesters_2:
        result_semesters.append(i)
        if i.Semester == get_semester.Semester:
            break

    credit_dict = {}
    gpa_dict = {}
    all_students = Student_data.objects.filter(session=get_batch)
    for student in all_students:
        credit_dict[student.Reg_No] = 0.00
        gpa_dict[student.Reg_No] = 0.00

    for j in result_semesters:
        student_list_3 = j.result_table_set.filter(Name='Name')
        x = student_list_3[0]
        fieldlist = x.__dict__
        for field, value in fieldlist.items():
            if value == 'Credit':
                credit = field
            if value == 'Total Grade Point':
                total_point = field

        student_list_4 = j.result_table_set.all().exclude(Name='Name').order_by('Reg')
        for student in student_list_4:
            get_reg = getattr(student, 'Reg')
            get_credit = getattr(student, credit)
            get_total_point = getattr(student, total_point)

            previous_credit = credit_dict[get_reg]
            after_credit = previous_credit+float(get_credit)
            credit_dict[get_reg] = after_credit

            previous_points = gpa_dict[get_reg]
            after_points = previous_points+float(get_total_point)
            gpa_dict[get_reg] = after_points

    student_list_5 = get_semester.result_table_set.all().exclude(
        Name='Name').order_by('Reg')
    for stu in student_list_5:
        find_reg = stu.Reg
        find_credit = credit_dict[find_reg]
        find_points = gpa_dict[find_reg]

        if find_credit == 0:
            continue

        calculate_cgpa = find_points/find_credit
        GPA = round(calculate_cgpa, 2)

        if(GPA < 2.00):
            letter_grade = 'F'
        if(GPA >= 2.00 and GPA < 2.25):
            letter_grade = 'C-'
        if(GPA >= 2.25 and GPA < 2.50):
            letter_grade = 'C'
        if(GPA >= 2.50 and GPA < 2.75):
            letter_grade = 'C+'
        if(GPA >= 2.75 and GPA < 3.00):
            letter_grade = 'B-'
        if(GPA >= 3.00 and GPA < 3.25):
            letter_grade = 'B'
        if(GPA >= 3.25 and GPA < 3.50):
            letter_grade = 'B+'
        if(GPA >= 3.50 and GPA < 3.75):
            letter_grade = 'A-'
        if(GPA >= 3.75 and GPA < 4.00):
            letter_grade = 'A'
        if(GPA == 4.00):
            letter_grade = 'A+'

        setattr(stu, CGPA_credit, find_credit)
        setattr(stu, CGPA, GPA)
        setattr(stu, CGPA_grade, letter_grade)
        stu.save()


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def result_info(request, batch, semester):
    get_batch = Sessions.objects.get(Batch=batch)
    get_session = get_batch.Session
    get_dept = get_batch.dept
    get_syllabus = get_batch.syllabus
    semester_string = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester)
    get_x = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester_string)
    course_list = get_x.course_list_all_set.all()
    get_semester = Result_Semester_List.objects.get(
        session=get_batch, Semester=semester)
    get_courses = Course.objects.filter(
        Batch=get_batch, semester=str(semester_string), Course_type='Theory')

    drop_courses_list = []

    if semester == '3rd':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='1st')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

    if semester == '4th':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='2nd')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

    if semester == '5th':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='1st')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='3rd')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

    if semester == '6th':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='2nd')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='4th')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

    if semester == '7th':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='1st')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='3rd')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='5th')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

    if semester == '8th':
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='2nd')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='4th')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)
        drop_courses_list.append('----')
        get_sem = Course_Semester_List.objects.get(
            syllabus=get_syllabus, Semester='6th')
        drop_courses = get_sem.course_list_all_set.all()
        for i in drop_courses:
            drop_courses_list.append(i)

            # Phase 1 - First Line

    result_info = get_semester.result_table_set.filter(Name='Name')
    first_line = result_info[0]
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
    my_list.append(first_line.Reg)
    my_list.append(first_line.Name)

    for field, value in column_list.items():
        if field == phase_1_start:
            start = 1
        if start == 1:
            my_list.append(value)
        if field == phase_1_stop:
            break

    # Phase 2 - First Line
    phase_2_start = ''
    Y = 0
    for field, value in column_list.items():
        if Y == 1:
            phase_2_start = field
            break
        if value == 'Name':
            Y = 1

    for field, value in column_list.items():
        phase_2_stop = field
        if value == 'Cumulative Grade':
            break

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

    # Phase 1 - Students
    result_info_2 = get_semester.result_table_set.all().exclude(
        Name='Name').order_by('Reg')
    for i in result_info_2:
        my_list.append(i.Reg)
        my_list.append(i.Name)
        column_list = i.__dict__
        start = 0
        for field, value in column_list.items():
            if field == phase_1_start:
                start = 1
            if start == 1:
                if value is None:
                    value = ' '
                my_list.append(value)
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
                my_list.append(value)
            if field == phase_2_stop:
                break

        list_of_list.append(my_list)
        my_list = []

    val = 'result_info_table'
    teahcer_list = Teacher_name.objects.all()
    batch2 = Sessions.objects.get(Batch=batch)
    semester_list = Result_Semester_List.objects.filter(session=batch2)
    context = {
        'result_info': list_of_list,
        'val': val,
        'course_list': course_list,
        'drop_course_list': drop_courses_list,
        'teacher_list': teahcer_list,
        'batch': batch,
        'semester': semester,
        'courses': get_courses,
        'result_semester_list': semester_list,
    }

    if request.method == 'POST':
        if 'assign_course' in request.POST:
            course = request.POST.get('courses')
            teacher = request.POST.get('teacher')
            if course and teacher is not None:
                teacher_obj = Teacher_name.objects.get(teacher=teacher)
                get_course2 = course_list.get(course_code=course)
                type2 = get_course2.course_type
                assigned_course_list = Course.objects.filter(
                    Batch=get_batch, Course=course)
                if assigned_course_list:
                    messages.warning(
                        request, 'This course has been already assigned!')
                    return render(request, 'result_info.html', context)
                else:
                    New_course = Course(teacher=teacher_obj, Course=course, Batch=get_batch,
                                        Course_type=type2, semester=semester_string.Semester)
                    New_course.save()
                    if type2 == 'Theory':
                        find_course = Course.objects.get(
                            Course=course, Batch=get_batch)
                        student_list = Student_data.objects.filter(
                            session=get_batch)
                        for i in student_list:
                            theory_course = Course_Result_Theory(
                                course=find_course, batch=get_batch, Reg_No=i.Reg_No, Name=i.Name, semester=find_course.semester)
                            theory_course.save()

                    elif type2 == 'Sessional':
                        find_course = Course.objects.get(
                            Course=course, Batch=get_batch)
                        student_list = Student_data.objects.filter(
                            session=get_batch)
                        for i in student_list:
                            theory_course = Course_Result_Sessional(
                                course=find_course, batch=get_batch, Reg_No=i.Reg_No, Name=i.Name, semester=find_course.semester)
                            theory_course.save()

            return render(request, 'result_info.html', context)
        if 'add_drop_courses' in request.POST:
            get_drop_course = request.POST.get('drop_courses')
            if get_drop_course == '----':
                messages.warning(request, 'Please select a valid course!!!')
                return redirect('result_info', batch, semester)

            else:
                drop_course_GP = get_drop_course+' GP'
                drop_course_LG = get_drop_course+' LG'
                get_collumns = first_line.__dict__
                null_count = 0
                for field, value in get_collumns.items():
                    if value is None:
                        find_LG_field = field
                        null_count += 1
                        if null_count == 2:
                            break
                        else:
                            find_GP_field = find_LG_field

                setattr(first_line, find_GP_field, drop_course_GP)
                setattr(first_line, find_LG_field, drop_course_LG)
                first_line.save()
                return redirect('result_info', batch, semester)

        if 'calculate' in request.POST:
            print(semester) 
            print(type(semester))
            calculate_GPA(batch, semester)
            return redirect('result_info', batch, semester)

        if 'create_pdf' in request.POST:
            if semester == '1st':
                exam = '1st Year 1st Semester Final Examination '
            if semester == '2nd':
                exam = '1st Year 2nd Semester Final Examination '
            if semester == '3rd':
                exam = '2nd Year 1st Semester Final Examination '
            if semester == '4th':
                exam = '2nd Year 2nd Semester Final Examination '
            if semester == '5th':
                exam = '3rd Year 1st Semester Final Examination '
            if semester == '6th':
                exam = '3rd Year 2nd Semester Final Examination '
            if semester == '7th':
                exam = '4th Year 1st Semester Final Examination '
            if semester == '8th':
                exam = '4th Year 2nd Semester Final Examination '

            list_of_list2 = list_of_list

            size = len(list_of_list2)
            length = size-1
            list_of_list_03 = []
            index = 0
            list_collections = []
            list_of_list_03.append(list_of_list2[0])

            for i in list_of_list2:
                if(length == index):
                    list_of_list_03.append(i)
                    list_collections.append(list_of_list_03)
                if index == 0:
                    index += 1
                    continue
                list_of_list_03.append(i)
                if (index % 17 == 0):
                    list_collections.append(list_of_list_03)
                    list_of_list_03 = []
                    list_of_list_03.append(list_of_list2[0])
                index += 1

            desktop_path = os.environ['USERPROFILE'] + '\Desktop\\'
            if not os.path.exists(desktop_path+'Expeliarms'):
                os.makedirs(desktop_path+'Expeliarms')

            number = 1
            for i in list_collections:
                context2 = {
                    'result_info': i,
                    'session': get_session,
                    'dept': get_dept,
                    'exam': exam,
                }
                template = get_template('pdf.html')
                html = template.render(context2)
                string_1 = 'Results 0'+str(number)
                string_2 = '.pdf'
                download_path = desktop_path+'\Expeliarms\\'+string_1+string_2
                number += 1

                options = {
                    'page-size': 'LETTER',
                    'orientation': 'Landscape',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'custom-header': [
                        ('Accept-Encoding', 'gzip')
                    ],
                    'cookie': [
                        ('cookie-name1', 'cookie-value1'),
                        ('cookie-name2', 'cookie-value2'),
                    ],
                    'no-outline': None,
                }

                path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                pdfkit.from_string(html, download_path,
                                   options=options, configuration=config)

            merger = PdfFileMerger()
            for file in os.listdir(desktop_path+'\Expeliarms\\'):
                if file.endswith(".pdf"):
                    merger.append(desktop_path+'\Expeliarms\\'+file)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Result.pdf"'
            merger.write(response)
            merger.close()

            if os.path.exists(desktop_path+'Expeliarms'):
                shutil.rmtree(desktop_path+'Expeliarms')

            return response

    return render(request, 'result_info.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def course_result_details(request, batch, semester, course):
    get_batch = Sessions.objects.get(Batch=batch)
    get_course = Course.objects.get(Batch=get_batch, Course=course)
    student_list = get_course.course_result_theory_set.all()

    teahcer_list = Teacher_name.objects.all()
    val = 'course_result_details'
    context = {
        'student_list': student_list,
        'teacher_list': teahcer_list,
        'val': val,
    }
    if request.method == 'POST':
        if('assign_khata' in request.POST):
            part_A_teacher = request.POST.get('part_a')
            part_B_teacher = request.POST.get('part_b')
            if part_A_teacher == part_B_teacher:
                messages.warning(
                    request, 'Both part can not be assigned to the same teacher!!!')
                return redirect('course_result_details', batch, semester, course)
            else:
                get_teacher_A = Teacher_name.objects.get(
                    teacher=part_A_teacher)
                get_teacher_B = Teacher_name.objects.get(
                    teacher=part_B_teacher)
                New_Course = Course_Khata(teacher=get_teacher_A, batch=get_batch,
                                          semester=semester, Course_Code=course, Exam_Part='Part A')
                New_Course.save()
                New_Course = Course_Khata(teacher=get_teacher_B, batch=get_batch,
                                          semester=semester, Course_Code=course, Exam_Part='Part B')
                New_Course.save()
                messages.success(
                    request, 'Part A and Part B has been assigned successfully.')
                return redirect('course_result_details', batch, semester, course)

        if ('calculate' in request.POST):
            print(2)
            gpa = 0.00
            grade = ''
            for i in student_list:
                total_marks = i.Pre_Final_Total + i.Exam_Part_A + i.Exam_Part_B
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
            return redirect('course_result_details', batch, semester, course)

        if('submit' in request.POST):
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

            student_list = get_course.course_result_theory_set.all().filter(
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

            drop_student_list = get_course.course_result_theory_set.all().exclude(
                semester=course_semester)

            for i in drop_student_list:
                session_obj = i.batch
                semester2 = i.semester
                gp = i.Grade_point
                lg = i.Letter_grade
                registration = i.Reg_No
                find_semester = Result_Semester_List.objects.get(
                    session=session_obj, Semester=semester2)
                get_course = Course.objects.get(Course=course, Batch=get_batch)
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

            return redirect('result_info', batch, semester)

    return render(request, 'result_info.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def re_admission(request):
    depthead = Depthead.objects.get(user=request.user)
    dept = depthead.dept
    reg_list = Student_data.objects.filter(dept=str(dept)).order_by('Reg_No')
    # dept2=Dept.objects.get(dept=dept)
    sessions = Sessions.objects.filter(dept=dept).order_by('Session')

    context = {
        'reg_list': reg_list,
        'sessions': sessions,
    }
    if request.method == 'POST':
        get_reg = request.POST.get('registration_no')
        get_batch = request.POST.get('batch')
        get_session = Sessions.objects.get(Batch=get_batch)
        Result_Table.objects.filter(Reg=get_reg).delete()
        student_data_obj = Student_data.objects.get(Reg_No=get_reg)
        student_name = student_data_obj.Name
        student_data_obj.session = get_session
        student_data_obj.save()

        semester_list = Result_Semester_List.objects.filter(
            session=get_session)
        for i in semester_list:
            New_student = Result_Table(
                Reg=get_reg, Name=student_name, result_semester=i, batch=get_session)
            New_student.save()

        return redirect('re-add')

    return render(request, 're-add.html', context)


# previous
""" @login_required
@allowed_user(allowed_roles=['DeptHead'])
def results(request):
    batch_list = Student_Sessions.objects.all()
    group = Group.objects.get(name='DeptHead')
    context = {
        'batch_list': batch_list,
        'group': group
    }
    return render(request, 'results.html', context) """


""" @login_required
@allowed_user(allowed_roles=['DeptHead'])
def batch_results(request, Dy_id):
    string = Dy_id
    context = {
        'string': string,
    }
    return render(request, 'semester_list.html', context) """


""" @ login_required


@allowed_user(allowed_roles=['DeptHead']) """


""" def calculate(batch, start, end, credit, point, grade):
    for i in batch.batch_result_set.all():
        credit_count = 0
        sem_1_total_gpa = 0
        fieldList = i._meta.get_fields()
        for field in fieldList[start:]:
            if (field.name == end):
                break
            GP = 'GP'
            if(GP in field.name):
                course_name = field.name
                course_name_01 = course_name[:-3]
                course_name_02 = course_name_01.replace('_', ' ')
                find_course = Course_list.objects.get(pk=course_name_02)
                find_credit = find_course.credit
                course_gpa = getattr(i, course_name)
                if (course_gpa is None):
                    continue
                if(course_gpa >= 2.00):
                    sem_1_total_gpa += course_gpa*find_credit
                    credit_count += find_credit
        if(credit_count == 0):
            break
        sem_1_GPA_full = sem_1_total_gpa/credit_count
        sem_1_GPA = round(sem_1_GPA_full, 2)

        if(sem_1_GPA < 2.00):
            letter_grade = 'F'
        if(sem_1_GPA >= 2.00 and sem_1_GPA < 2.25):
            letter_grade = 'C-'
        if(sem_1_GPA >= 2.25 and sem_1_GPA < 2.50):
            letter_grade = 'C'
        if(sem_1_GPA >= 2.50 and sem_1_GPA < 2.75):
            letter_grade = 'C+'
        if(sem_1_GPA >= 2.75 and sem_1_GPA < 3.00):
            letter_grade = 'B-'
        if(sem_1_GPA >= 3.00 and sem_1_GPA < 3.25):
            letter_grade = 'B'
        if(sem_1_GPA >= 3.25 and sem_1_GPA < 3.50):
            letter_grade = 'B+'
        if(sem_1_GPA >= 3.50 and sem_1_GPA < 3.75):
            letter_grade = 'A-'
        if(sem_1_GPA >= 3.75 and sem_1_GPA < 4.00):
            letter_grade = 'A'
        if(sem_1_GPA == 4.00):
            letter_grade = 'A+'

        setattr(i, credit, credit_count)
        setattr(i, point, sem_1_GPA)
        setattr(i, grade, letter_grade)
        i.save()
        sem_1_GPA = 0
        letter_grade = ' '


def get_courses(sem):
    course_list_01 = Course_list.objects.filter(semester=sem)
    course_list_02 = []
    course_list_03 = []
    for i in course_list_01:
        string01 = i.course_code
        string02 = string01.replace(' ', '_')
        course_list_02.append(string01)
        course_list_03.append(string02)

    course_list_zip = zip(course_list_02, course_list_03)
    return course_list_zip


def get_teachers():
    teacher_list_01 = Teacher.objects.all()
    teacher_list_02 = []
    teacher_list_03 = []
    for j in teacher_list_01:
        string03 = j.Name
        string04 = string03.replace(' ', '_')
        teacher_list_02.append(string03)
        teacher_list_03.append(string04)

    teacher_list_zip = zip(teacher_list_02, teacher_list_03)
    return teacher_list_zip """


""" @ login_required
@allowed_user(allowed_roles=['DeptHead']) """


""" def assign_teacher(string01, string02, string03):
    course = string01
    teacher = string02
    Dy_id = string03
    course_02 = course.replace('_', ' ')
    teacher_02 = teacher.replace('_', ' ')
    teacher_03 = Teacher.objects.get(Name=teacher_02)
    sess = Student_Sessions.objects.get(Batch=Dy_id)
    new_course = Course(Session=sess.Session, Course=course_02,
                        Batch=Dy_id, teacher=teacher_03)
    new_course.save()
    find_course = Course.objects.get(Batch=Dy_id, Course=course_02)
    for i in Student_data.objects.filter(session=Dy_id):
        reg = i.Reg_No
        name = i.Name
        new_student = Course_Result_Theory(
            course=find_course, Reg_No=reg, Name=name)
        new_student.save()
    string04 = 'Teachers '+Dy_id
    teacher_entry_tuple = batch_result.objects.get_or_create(
        Reg_No=string04, Result_Session=sess)
    teacher_entry = teacher_entry_tuple[0]
    course02 = course+"_LG"
    setattr(teacher_entry, course02, teacher_02)
    teacher_entry.save() """


""" @login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_01(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('1st')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 2
            End = 'Sem_01_Total_Credit'
            Credit_Field = 'Sem_01_Total_Credit'
            Point_Field = 'Sem_01_Grade_Point'
            Grade_Field = 'Sem_01_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    context = {
        'result_list': batch4,
        'course_list': course_list,
        'teacher_list': teacher_list,
        'group': group
    }
    return render(request, 'semester_01.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_02(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('2nd')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 28
            End = 'Sem_02_Total_Credit'
            Credit_Field = 'Sem_02_Total_Credit'
            Point_Field = 'Sem_02_Grade_Point'
            Grade_Field = 'Sem_02_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Sem_02_Total_Credit'
            Credit_Field = 'Total_Credit_Till_Sem_02'
            Point_Field = 'Grade_Point_Till_Sem_02'
            Grade_Field = 'Letter_Grade_Till_Sem_02'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_02.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_03(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('3rd')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 52
            End = 'Sem_03_Total_Credit'
            Credit_Field = 'Sem_03_Total_Credit'
            Point_Field = 'Sem_03_Grade_Point'
            Grade_Field = 'Sem_03_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Sem_03_Total_Credit'
            Credit_Field = 'Total_Credit_Till_Sem_03'
            Point_Field = 'Grade_Point_Till_Sem_03'
            Grade_Field = 'Letter_Grade_Till_Sem_03'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_03.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_04(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('4th')
    teacher_list = get_teachers()
    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 76
            End = 'Sem_04_Total_Credit'
            Credit_Field = 'Sem_04_Total_Credit'
            Point_Field = 'Sem_04_Grade_Point'
            Grade_Field = 'Sem_04_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Sem_04_Total_Credit'
            Credit_Field = 'Total_Credit_Till_Sem_04'
            Point_Field = 'Grade_Point_Till_Sem_04'
            Grade_Field = 'Letter_Grade_Till_Sem_04'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_04.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_05(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('5th')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 100
            End = 'Z1_Sem_05_Total_Credit'
            Credit_Field = 'Z1_Sem_05_Total_Credit'
            Point_Field = 'Z2_Sem_05_Grade_Point'
            Grade_Field = 'Z3_Sem_05_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Z1_Sem_05_Total_Credit'
            Credit_Field = 'Z4_Total_Credit_Till_Sem_05'
            Point_Field = 'Z5_Grade_Point_Till_Sem_05'
            Grade_Field = 'Z6_Letter_Grade_Till_Sem_05'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_05.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_06(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('6th')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 124
            End = 'Z1_Sem_06_Total_Credit'
            Credit_Field = 'Z1_Sem_06_Total_Credit'
            Point_Field = 'Z2_Sem_06_Grade_Point'
            Grade_Field = 'Z3_Sem_06_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Z1_Sem_06_Total_Credit'
            Credit_Field = 'Z4_Total_Credit_Till_Sem_06'
            Point_Field = 'Z5_Grade_Point_Till_Sem_06'
            Grade_Field = 'Z6_Letter_Grade_Till_Sem_06'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_06.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_07(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('7th')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 148
            End = 'Z1_Sem_07_Total_Credit'
            Credit_Field = 'Z1_Sem_07_Total_Credit'
            Point_Field = 'Z2_Sem_07_Grade_Point'
            Grade_Field = 'Z3_Sem_07_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Z1_Sem_07_Total_Credit'
            Credit_Field = 'Z4_Total_Credit_Till_Sem_07'
            Point_Field = 'Z5_Grade_Point_Till_Sem_07'
            Grade_Field = 'Z6_Letter_Grade_Till_Sem_07'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_07.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def semester_08(request, Dy_id):
    Batch = Student_Sessions.objects.get(pk=Dy_id)
    course_list = get_courses('8th')
    teacher_list = get_teachers()

    if (request.method == 'POST'):
        if('cal_GPA' in request.POST):
            Start = 180
            End = 'Z1_Sem_08_Total_Credit'
            Credit_Field = 'Z1_Sem_08_Total_Credit'
            Point_Field = 'Z2_Sem_08_Grade_Point'
            Grade_Field = 'Z3_Sem_08_LG'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

            Start = 2
            End = 'Z1_Sem_08_Total_Credit'
            Credit_Field = 'Z4_Total_Credit_Till_Sem_08'
            Point_Field = 'Z5_Grade_Point_Till_Sem_08'
            Grade_Field = 'Z6_Letter_Grade_Till_Sem_08'
            calculate(Batch, Start, End, Credit_Field,
                      Point_Field, Grade_Field)

        if('assign_course' in request.POST):
            course = request.POST['course']
            teacher = request.POST['teacher']
            bat = Batch.Batch
            cou = course.replace("_", ' ')
            if Course.objects.filter(Course=cou, Batch=bat).exists():
                messages.error(
                    request, "This Course Has Been Already Assigned", extra_tags='teacher')
                return redirect(request.path)
            assign_teacher(course, teacher, Dy_id)

    batch2 = Student_Sessions.objects.get(pk=Dy_id)
    batch3 = batch2.batch_result_set.all()
    if batch3.exists() == False:
        messages.error(
            request, "No Student in this session has been added yet", extra_tags='student')
    batch4 = sorted(batch3, key=lambda batch_result: batch_result.Reg_No)
    group = Group.objects.get(name='DeptHead')
    return render(request, 'semester_08.html', {'result_list': batch4, 'course_list': course_list, 'teacher_list': teacher_list, 'group': group})
 """
