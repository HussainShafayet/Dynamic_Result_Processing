from django.shortcuts import render, redirect
from django.contrib.auth.models import (User, Group,)
from accounts.models import (Student, Teacher)
from django.contrib.auth import get_user_model
from .forms import (AddCourse,Create_batch)
from .models import (Course_list, Batch, Session,Student_Sessions,batch_result,Dept)
from teacher.models import (Teachers, Course, Course_Result)
from student.models import(Students)
from django.contrib import messages

# Create your views here.

def depthead_home(request):
    return render(request, 'user_Dashboard.html', {'val': 'user_dh',})
    
#Users,Userdetails and Allowuser
def users(request):
    if request.method == 'POST':
        q = request.GET['search']
        print(2)
        print(q)
        User = get_user_model()
        user_list = User.objects.filter(groups__name='None')
        val = 'user_val'
        context = {
            'user_list': user_list,
            'val': val
        }
        return render(request, 'users.html', context)
    else:
        User = get_user_model()
        user_list = User.objects.filter(groups__name='None')
        val = 'user_val'
        context = {
            'user_list': user_list,
            'val': val
        }
        return render(request, 'users.html', context)

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
            name1 = user_det.first_name
            name2 = user_det.last_name
            name = name1 + ' ' + name2
            Add_Teacher = Teachers(Name=name)
            Add_Teacher.save()
            return redirect('users')
        elif grop_name == 'Student':
            group = Group.objects.get(name='Student')
            user_det.groups.add(group)
            g = Group.objects.get(name='None')
            user_det.groups.remove(g)
            user_det.is_none = False
            user_det.is_student = True
            user_det.save()
            n1=user_det.first_name
            n2 = user_det.last_name
            name = n1 + ' ' + n2
            stud = Student.objects.get(user=user_det)
            dept = Dept.objects.get(dept=stud.dept)
            batch = stud.batch
            Sess = Student_Sessions.objects.get(Batch=batch)
            New_Student = Students(
                Reg_No=stud.reg_no, Name=name, Gender=stud.gender, Dept=dept,Phone=stud.mobile, session=Sess)
            New_Student.save()
            Result_Table = batch_result(Reg_No=stud.reg_no, Name=name, Result_Session=Sess)
            Result_Table.save()
            return redirect('users')
    else:
        user_det = User.objects.get(id=id)
    context = {
        'user_det': user_det,
        'val': 'user_details'
    }
    return render(request, 'users.html', context)


def student_info(request):
    User = get_user_model()
    stud_info = User.objects.filter(groups__name='Student')
    val = 'std_info'
    context = {
        'stud_info': stud_info,
        'val': val
    }
    return render(request, 'users.html', context)


def teacher_info(request):
    User = get_user_model()
    teaher_info = User.objects.filter(groups__name='Teacher')
    val = 'teach_info'
    context = {
        'teaher_info': teaher_info,
        'val': val
    }
    return render(request, 'users.html', context)
#Course create and Show


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
        return render(request, 'course.html', context)

def show_course(request): 
    course_list = Course_list.objects.all().order_by('semester','course_code')
    val = 'course_li'
    context = {
        'course_list': course_list,
        'val': val
    }
    return render(request, 'course.html', context)


def create_batch(request):
    if request.method == 'POST':
        form = Create_batch(request.POST)
        if form.is_valid():
            batch = form.cleaned_data['Batch']
            session = form.cleaned_data['Session']
            form.save()
            add_batch = Batch(batch=batch)
            add_batch.save()
            add_session = Session(session=session)
            add_session.save()
            return redirect('depthead_dashboard')
        else:
            context = {
                'form':form,
            }
            return render(request, 'create_batch.html', context)
    else:
        form = Create_batch()
        context = {
            'form':form,
        }
        return render(request, 'create_batch.html',context)


def batch_info(request, Dy_id):
    batch = Student_Sessions.objects.get(pk=Dy_id)
    query_set = batch.students_set.all()
    if query_set.exists() == False:
        messages.error(
            request, "No Student of this session has been added yet")
    return render(request, 'batch_info.html', {'student_list': batch,})

def find_batch(request):
    batches = Batch.objects.all()
    return render(request,'base.html',{'batches':batches})


def show_batch(request):
    batch_session = Batch.objects.all()
    val = 'show_batch'
    contex = {
        'batch_session': batch_session,
        'val': val,
    }
    return render(request, 'depthead.html', contex)


def results(request):
    batch_list = Student_Sessions.objects.all()
    group = Group.objects.get(name='DeptHead')
    context = {
        'batch_list': batch_list,
        'group': group
    }
    return render(request, 'results.html', context)


def batch_results(request, Dy_id):
    string = Dy_id
    group = Group.objects.get(name='DeptHead')
    context = {
        'string': string,
        'group': group,

    }
    return render(request, 'semester_list.html', context)


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
    teacher_list_01 = Teachers.objects.all()
    teacher_list_02 = []
    teacher_list_03 = []
    for j in teacher_list_01:
        string03 = j.Name
        string04 = string03.replace(' ', '_')
        teacher_list_02.append(string03)
        teacher_list_03.append(string04)

    teacher_list_zip = zip(teacher_list_02, teacher_list_03)
    return teacher_list_zip


def assign_teacher(string01, string02, string03):
    print(2)
    course = string01
    teacher = string02
    Dy_id = string03
    course_02 = course.replace('_', ' ')
    teacher_02 = teacher.replace('_', ' ')
    teacher_03 = Teachers.objects.get(Name=teacher_02)
    sess = Student_Sessions.objects.get(Batch=Dy_id)
    new_course = Course(Session=sess.Session, Course=course_02,
                        Batch=Dy_id, teacher=teacher_03)
    new_course.save()
    find_course = Course.objects.get(Batch=Dy_id, Course=course_02)
    for i in Students.objects.filter(session=Dy_id):
        reg = i.Reg_No
        name = i.Name
        new_student = Course_Result(course=find_course, Reg_No=reg, Name=name)
        new_student.save()
    """ string04='Teachers '+Dy_id
    teacher_entry_tuple = batch_result.objects.get_or_create(Reg_No=string04,Result_Session=sess)
    teacher_entry = teacher_entry_tuple[0]
    course02 = course+"_LG"
    setattr(teacher_entry, course02, teacher_02)
    teacher_entry.save() """


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
