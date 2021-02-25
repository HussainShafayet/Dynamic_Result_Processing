from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import (User, Group,)
from accounts.models import (Student, Teacher, Depthead)
from django.contrib.auth import get_user_model
from .forms import (AddCourse, Create_batch, AddSyllabus, Add_Semester)
from .models import (Course_list, Batch, Session,
                     Student_Sessions, batch_result, Dept, Syllabus, Course_Semester_List, Sessions, Result_Semester_List, Result_Table, Course_List_All)
from teacher.models import (
    Course, Course_Result_Theory, Course_Result_Sessional, Teacher_name)
from student.models import(Students)
from django.contrib import messages
from .decorators import login_required, allowed_user
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response
# Create your views here.


def depthead_home(request):
    return render(request, 'user_Dashboard.html', {'val': 'user_dh', })

#Users,Userdetails and Allowuser


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
            User = get_user_model()
            user_list = User.objects.filter(groups__name='None')
            val = 'user_val'
            context = {
                'user_list': user_list,
                'val': val,
            }
            return render(request, 'users.html', context)

    else:
        User = get_user_model()
        user_list = User.objects.filter(groups__name='None')
        val = 'user_val'
        context = {
            'user_list': user_list,
            'val': val,
        }
        return render(request, 'users.html', context)


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
            get_sess = Sessions.objects.get(Batch=batch)
            semester_list = Result_Semester_List.objects.filter(
                session=get_sess)
            for i in semester_list:
                New_student = Result_Table(
                    Reg=reg, Name=name, result_semester=i)
                New_student.save()
            return redirect('users')
    else:
        user_det = User.objects.get(id=id)
    context = {
        'user_det': user_det,
        'val': 'user_details'
    }
    return render(request, 'users.html', context)


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
            group = Group.objects.get(name='Student')
            User = get_user_model()
            stud_info = User.objects.filter(groups=group).filter(
                Q(first_name__icontains=str(q)) | Q(last_name__icontains=str(q)) | Q(username__icontains=q) | Q(email__icontains=str(q)))
            if stud_info:
                val = 'std_info'
                context = {
                    'stud_info': stud_info,
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
            User = get_user_model()
            stud_info = User.objects.filter(groups__name='Student')
            val = 'std_info'
            context = {
                'stud_info': stud_info,
                'val': val,
            }
            return render(request, 'users.html', context)
    else:
        User = get_user_model()
        stud_info = User.objects.filter(groups__name='Student')
        val = 'std_info'
        context = {
            'stud_info': stud_info,
            'val': val,
        }
        return render(request, 'users.html', context)


def student_search(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        User = get_user_model()
        user_list = User.objects.filter(groups__name='Student').filter(
            Q(first_name__icontains=search_str) | Q(last_name__icontains=str(search_str)) | Q(username__icontains=str(search_str)) | Q(email__icontains=str(search_str)))
        data = user_list.values()
        return JsonResponse(list(data), safe=False)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def teacher_info(request):
    if 'search' in request.GET:
        q = request.GET.get('search')
        if q:
            group = Group.objects.get(name='Teacher')
            User = get_user_model()
            teacher_info = User.objects.filter(groups=group).filter(
                Q(first_name__icontains=str(q)) | Q(last_name__icontains=str(q)) | Q(username__icontains=str(q)) | Q(email__icontains=str(q)))
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
            User = get_user_model()
            teacher_info = User.objects.filter(groups__name='Teacher')
            val = 'teach_info'
            context = {
                'teacher_info': teacher_info,
                'val': val,
            }
            return render(request, 'users.html', context)
    else:
        User = get_user_model()
        teacher_info = User.objects.filter(groups__name='Teacher')
        val = 'teach_info'
        context = {
            'teacher_info': teacher_info,
            'val': val,
        }
        return render(request, 'users.html', context)


def teacher_search(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        User = get_user_model()
        user_list = User.objects.filter(groups__name='Teacher').filter(
            Q(first_name__icontains=search_str) | Q(last_name__icontains=str(search_str)) | Q(username__icontains=str(search_str)) | Q(email__icontains=str(search_str)))
        data = user_list.values()
        return JsonResponse(list(data), safe=False)

# add Syllabus and view syllabus


def add_syllabus(request):
    if request.method == 'POST':
        form = AddSyllabus(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Add successfully!')
            return redirect('syllabus')
        else:
            messages.warning(request, 'Try again!')
            val = 'add_syllabus'
            context = {
                'form': form,
                'val': val,
            }
        return render(request, 'syllabus.html', context)
    else:
        form = AddSyllabus()
        val = 'add_syllabus'
        context = {
            'form': form,
            'val': val,
        }
        return render(request, 'syllabus.html', context)


def view_syllabus(request):
    depthead = Depthead.objects.get(user=request.user)
    dept = depthead.dept
    syllabus = Syllabus.objects.filter(dept=dept)
    val = 'view_syllabus'
    context = {
        'syllabus': syllabus,
        'val': val,
    }
    return render(request, 'syllabus.html', context)


def syllabus_semester(request, syllabus_id):
    syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
    semester = Course_Semester_List.objects.filter(syllabus=syllabus)
    syllabus_id = syllabus_id
    val = 'syllabus_semester'
    context = {
        'semester': semester,
        'val': val,
        'syllabus_id': syllabus_id,
    }
    return render(request, 'syllabus.html', context)


def add_semester(request, syllabus_id):
    if request.method == 'POST':
        form = Add_Semester(request.POST, syllabus_id)
        if form.is_valid():
            get_syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
            semester = form.cleaned_data['Semester']
            get_sem = Course_Semester_List.objects.filter(
                syllabus=get_syllabus, Semester=semester)
            if get_sem:
                messages.warning(request, 'This semester already exists!')
                val = 'add_semester'
                context = {
                    'form': form,
                    'val': val,
                    'syllabus_id': syllabus_id,
                }
                return render(request, 'syllabus.html', context)
            else:
                New_Course_Semester_List = Course_Semester_List(
                    syllabus=get_syllabus, Semester=semester)
                New_Course_Semester_List.save()
                messages.success(request, 'Semester added successfully!')
                return redirect('syllabus_semester', syllabus_id)
        else:
            messages.warning(request, 'Try again!')
            val = 'add_semester'
            context = {
                'form': form,
                'val': val,
                'syllabus_id': syllabus_id,
            }
            return render(request, 'syllabus.html', context)
    else:
        form = Add_Semester()
        val = 'add_semester'
        context = {
            'form': form,
            'val': val,
            'syllabus_id': syllabus_id,
        }
        return render(request, 'syllabus.html', context)


def view_course_list_all(request, syllabus_id, semester):
    syllabus = Syllabus.objects.get(Syllabus_Name=syllabus_id)
    get_semester = Course_Semester_List.objects.get(
        syllabus=syllabus, Semester=semester)
    course_list = get_semester.course_list_all_set.all()
    val = 'course_list_by_semester'
    context = {
        'course_list': course_list,
        'val': val,
        'semester': semester,
        'syllabus_id': syllabus_id
    }
    return render(request, 'course_list.html', context)


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


# Course create and Show
""" @login_required
@allowed_user(allowed_roles=['DeptHead'])
def addcourse(request):
    if request.method == 'POST':
        form = AddCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course')
        else:
            context = {
                'form': form,
            }
            return render(request, 'course.html', context)
    else:
        form = AddCourse()
        context = {
            'form': form
        }
        return render(request, 'course.html', context) """


""" @login_required
@allowed_user(allowed_roles=['DeptHead'])
def show_course(request):
    course_list = Course_list.objects.all().order_by('semester', 'course_code')
    val = 'course_li'
    context = {
        'course_list': course_list,
        'qs_json': json.dumps(list(course_list.values()), cls=DjangoJSONEncoder),
        'val': val,
    }
    return render(request, 'course.html', context) """


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def create_batch(request):
    if request.method == 'POST':
        form = Create_batch(request.POST)
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
                    result_semester=i, Reg=string_03, Name=string_Name)
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
                courses_02.append("Total Credit")
                courses_02.append("Grade Point")
                courses_02.append("Letter Grade")

                for j in i.result_table_set.all():
                    fieldList1 = j._meta.get_fields()
                    fieldList2 = fieldList1[4:]
                    Two_list = zip(fieldList2, courses_02)
                    for l, m in Two_list:
                        string_06 = l.name
                        string_07 = m
                        setattr(j, string_06, string_07)
                        j.save()

            """ form.save()
            add_batch = Batch(batch=batch)
            add_batch.save()
            add_session = Session(session=session)
            add_session.save() """
            return redirect('find_batch')
        else:
            messages.warning(request, 'Try again!')
            context = {
                'form': form,
            }
            return render(request, 'create_batch.html', context)
    else:
        form = Create_batch()
        context = {
            'form': form,
        }
        return render(request, 'create_batch.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def find_batch(request):
    depthead = Depthead.objects.get(user=request.user)
    dept = depthead.dept
    batches = Sessions.objects.filter(dept=dept)
    val = 'batch_info'
    context = {
        'batches': batches,
        'val': val
    }
    return render(request, 'batch_info.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def batch_info(request, batch):
    batch2 = Sessions.objects.get(Batch=batch)
    semester_list = Result_Semester_List.objects.filter(session=batch2)
    #result_semester_list = batch.result_semester_list_set.all()

    context = {
        'result_semester_list': semester_list,
        'val': 'result_semester_list_info',
        'batch_val': batch

    }
    return render(request, 'batch_info.html', context)


def result_info(request, batch, semester):
    get_batch = Sessions.objects.get(Batch=batch)
    get_syllabus = get_batch.syllabus
    semester_string = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester)
    get_x = Course_Semester_List.objects.get(
        syllabus=get_syllabus, Semester=semester_string)
    course_list = get_x.course_list_all_set.all()
    get_semester = Result_Semester_List.objects.get(
        session=get_batch, Semester=semester)
    result_info = get_semester.result_table_set.all()
    list_of_list = []
    list1 = []
    for i in result_info:
        field_list = i._meta.get_fields()
        for j in field_list[2:]:
            val = getattr(i, j.name)
            if val == None:
                break
            else:
                list1.append(val)
        list_of_list.append(list1)
        list1 = []
        val = 'result_info_table'
        teahcer_list = Teacher_name.objects.all()
        context = {
            'result_info': list_of_list,
            'val': val,
            'course_list': course_list,
            'teacher_list': teahcer_list,
            'batch': batch,
            'semester': semester
        }

    if request.method == 'POST':
        course = request.POST.get('courses')
        teacher = request.POST.get('teacher')
        teacher_obj = Teacher_name.objects.get(teacher=teacher)
        get_course2 = course_list.get(course_code=course)
        type2 = get_course2.course_type
        assigned_course_list = Course.objects.filter(
            Batch=get_batch, Course=course)
        if assigned_course_list:
            messages.warning(request, 'This course has been already assigned!')
            return render(request, 'result_info.html', context)
        else:
            New_course = Course(teacher=teacher_obj, Course=course,
                                Batch=get_batch, Course_type=type2)
            New_course.save()
    return render(request, 'result_info.html', context)


# previous
@login_required
@allowed_user(allowed_roles=['DeptHead'])
def results(request):
    batch_list = Student_Sessions.objects.all()
    group = Group.objects.get(name='DeptHead')
    context = {
        'batch_list': batch_list,
        'group': group
    }
    return render(request, 'results.html', context)


@login_required
@allowed_user(allowed_roles=['DeptHead'])
def batch_results(request, Dy_id):
    string = Dy_id
    context = {
        'string': string,
    }
    return render(request, 'semester_list.html', context)


""" @login_required
@allowed_user(allowed_roles=['DeptHead']) """


def calculate(batch, start, end, credit, point, grade):
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
    return teacher_list_zip


""" @login_required
@allowed_user(allowed_roles=['DeptHead']) """


def assign_teacher(string01, string02, string03):
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
    for i in Students.objects.filter(session=Dy_id):
        reg = i.Reg_No
        name = i.Name
        new_student = Course_Result_Theory(
            course=find_course, Reg_No=reg, Name=name)
        new_student.save()
    """ string04='Teachers '+Dy_id
    teacher_entry_tuple = batch_result.objects.get_or_create(Reg_No=string04,Result_Session=sess)
    teacher_entry = teacher_entry_tuple[0]
    course02 = course+"_LG"
    setattr(teacher_entry, course02, teacher_02)
    teacher_entry.save() """


@login_required
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
