from django.shortcuts import render, redirect
from django.contrib.auth.models import (User, Group,)
from accounts.models import (Student, Teacher)
from django.contrib.auth import get_user_model
from .forms import (Course,Create_batch)
from .models import (Course_List,Batch)

# Create your views here.


def depthead_home(request):
    return render(request, 'user_Dashboard.html', {'val': 'user_dh'})
#Users,Userdetails and Allowuser


def users(request):
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
            return redirect('users')
        elif grop_name == 'Student':
            group = Group.objects.get(name='Student')
            user_det.groups.add(group)
            g = Group.objects.get(name='None')
            user_det.groups.remove(g)
            user_det.is_none = False
            user_det.is_student = True
            user_det.save()
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


def course(request):
    if request.method == 'POST':
        form = Course(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course')
        else:
            context = {
                'form': form,
            }
            return render(request, 'course.html', context)
    else:
        form = Course()
        context = {
            'form': form
        }
        return render(request, 'course.html', context)


def show_course(request):
    course_list = Course_List.objects.all()
    val = 'course_li'
    context = {
        'course_list': course_list,
        'val': val
    }
    return render(request, 'course.html', context)


def createbatch(request):
    if request.method == 'POST':
        form = Create_batch(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            val = 'crt_batch'
            context = {
                'form': form,
                'val': val
            }
            return render(request, 'depthead.html', context)
    else:
        form = Create_batch()
        val = 'crt_batch'
        context = {
            'form': form,
            'val': val,
        }
        return render(request, 'depthead.html', context)


def show_batch(request):
    batch_session = Batch.objects.all()
    val = 'show_batch'
    contex = {
        'batch_session': batch_session,
        'val': val,
    }
    return render(request, 'depthead.html', contex)
