from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
# User Reg,login and Logout
from .forms import (DeptheadRegForm, TeacherRegForm, StudentRegForm, Profile_edit_Form,
                    Depthead_profile_edit_form, Teacher_profile_edit_form, Student_profile_edit_form)
from .models import (User, Teacher, Student, Depthead)
from depthead.models import (Dept, Batch, Session)
from student.models import(Student_data)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    login, logout, authenticate, update_session_auth_hash)
from django.contrib.auth.models import (auth, Group)
# Reset Password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeForm)
# Accounts Activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Decorators
from depthead.decorators import unauthenticated_user, login_required

# My views here.

def home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_depthead:
            return redirect('depthead_dashboard')
        elif user.is_student:
            return redirect('student_dashboard')
        elif user.is_teacher:
            return redirect('teacher_dashboard')
    else:    
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_depthead:
                        auth.login(request, user)
                        messages.success(request, 'You are logged in!')
                        return redirect('depthead_dashboard')
                    elif user.is_student:
                        auth.login(request, user)
                        messages.success(request, 'You are logged in!')
                        return redirect('student_dashboard')
                    elif user.is_teacher:
                        auth.login(request, user)
                        messages.success(request, 'You are logged in!')
                        return redirect('teacher_dashboard')
                    else:
                        auth.login(request, user)
                        messages.warning(request, 'Your are not authorised user')
                        return redirect(home)
            else:
                conext = {
                    'form': form
                }
                return render(request, 'login.html', conext)
        else:
            form = AuthenticationForm()
            conext = {
                'form': form
            }
        return render(request, 'user_dashboard.html',conext)

def about(request):
    return render(request,'about.html')

# User Registration and Activation


def depthead_registraion(request):
    if request.method == 'POST':
        form = DeptheadRegForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='None')
            user.groups.add(group)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            val = 1
            context = {
                'val': val
            }
            return render(request, 'active_account.html', context)
        else:
            val = 'depthead_reg'
            context = {
                'form': form,
                'val': val,
            }
            return render(request, 'registration.html', context)
    else:
        form = DeptheadRegForm()
        val = 'depthead_reg'
        context = {
            'form': form,
            'val': val,
        }
    return render(request, 'registration.html', context)


@unauthenticated_user
def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherRegForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            group = Group.objects.get(name='None')
            user.groups.add(group)
            messages.success(request, 'Registration Successful !!!')
            return redirect('login')
            """ current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            val=1
            context = {
                'val':val
            }
            return render(request,'active_account.html',context) """
        else:
            val = 'teacher_reg'
            context = {
                'form': form,
                'val': val,
            }
            return render(request, 'registration.html', context)
    else:
        form = TeacherRegForm()
        val = 'teacher_reg'
    context = {
        'form': form,
        'val': val
    }
    return render(request, 'registration.html', context)


def ajax(request):
    if request.is_ajax():
        term = request.GET.get('term')
        dept = Dept.objects.all().filter(dept__icontains=term)
        response_content = list(dept.values())
        return JsonResponse(response_content, safe=False)


def ajax2(request):
    if request.is_ajax():
        term = request.GET.get('term')
        batch = Batch.objects.all().filter(batch__icontains=term)
        response_content = list(batch.values())
        return JsonResponse(response_content, safe=False)


def ajax3(request):
    if request.is_ajax():
        term = request.GET.get('term')
        session = Session.objects.all().filter(session__icontains=term)
        response_content = list(session.values())
        return JsonResponse(response_content, safe=False)


@unauthenticated_user
def student_registration(request):
    if request.method == 'POST':
        form = StudentRegForm(request.POST, request.FILES)
        if form.is_valid():
            reg_no = form.cleaned_data.get('reg_no')
            reg_no_test = Student_data.objects.filter(Reg_No=reg_no)
            if reg_no_test:
                messages.warning(
                    request, 'Registration Number already Exists!')
                val = 'student_reg'
                context = {
                    'form': form,
                    'val': val,
                }
                return render(request, 'registration.html', context)
            else:
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                group = Group.objects.get(name='None')
                user.groups.add(group)
                messages.success(request, 'Registration Successful !!!')
                return redirect('login')
                """ current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject,message,to=[to_email])
                email.send()
                val = 1
                context = {
                    'val': val
                }
                return render(request, 'active_account.html', context) """
        else:
            messages.warning(request, 'Try again!')
            val = 'student_reg'
            context = {
                'form': form,
                'val': val,
            }
            return render(request, 'registration.html', context)
    else:
        form = StudentRegForm()
        val = 'student_reg'
    context = {
        'form': form,
        'val': val,
    }
    return render(request, 'registration.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Registration successful!')
        return render(request, 'active_account.html', {'val': 2})
    else:
        return render(request, 'active_account.html')


# User Login and Logout

@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_depthead:
                    auth.login(request, user)
                    messages.success(request, 'You are logged in!')
                    return redirect('depthead_dashboard')
                elif user.is_student:
                    auth.login(request, user)
                    messages.success(request, 'You are logged in!')
                    return redirect('student_dashboard')
                elif user.is_teacher:
                    auth.login(request, user)
                    messages.success(request, 'You are logged in!')
                    return redirect('teacher_dashboard')
                else:
                    auth.login(request, user)
                    messages.warning(request, 'Your are not authorised user')
                    return redirect(home)
        else:
            conext = {
                'form': form
            }
            return render(request, 'login.html', conext)
    else:
        form = AuthenticationForm()
        conext = {
            'form': form
        }
        return render(request, 'login.html', conext)


def user_logout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('home')

# Reset Password


class ResetPassword(UserPassesTestMixin, PasswordResetView):
    template_name = 'password_reset.html'

    def test_func(self):
        return self.request.user.is_anonymous


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


@login_required
def profile(request):
    current_user = request.user
    if current_user.is_depthead:
        profile_value = Depthead.objects.get(user=current_user)
        user = User.objects.get(username=current_user)
        profile_details = 'profile_details'
        context = {
            'profile_value': profile_value,
            'user': user,
            'profile_details': profile_details
        }
        return render(request, 'profile.html', context)

    elif current_user.is_teacher:
        profile_value = Teacher.objects.get(user=current_user)
        user = User.objects.get(username=current_user)
        profile_details = 'profile_details'
        context = {
            'profile_value': profile_value,
            'user': user,
            'profile_details': profile_details
        }
        return render(request, 'profile.html', context)
    elif current_user.is_student:
        profile_value = Student.objects.get(user=current_user)
        user = User.objects.get(username=current_user)
        profile_details = 'profile_details'
        context = {
            'profile_value': profile_value,
            'user': user,
            'profile_details': profile_details
        }
        return render(request, 'profile.html', context)
    else:
        return HttpResponse('You are not authorised user!')


@login_required
def profile_edit(request, id):
    if request.method == 'POST':
        current_user = User.objects.get(id=id)
        form = Profile_edit_Form(request.POST, instance=request.user)
        if current_user.is_depthead:
            profile = current_user.depthead
            form2 = Depthead_profile_edit_form(request.POST, instance=profile)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                messages.success(request, 'Profile update successfully!')
                return redirect('profile')
            else:
                messages.warning(request, 'Try again!!!')
                profile_value = Depthead.objects.get(user=request.user)
                context = {
                    'form': form,
                    'form2': form2,
                    'profile_value': profile_value,
                }
            return render(request, 'profile.html', context)
        elif current_user.is_teacher:
            profile = current_user.teacher
            form2 = Teacher_profile_edit_form(request.POST, instance=profile)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                messages.success(request, 'Profile update successfully!')
                return redirect('profile')
            else:
                profile_value = Teacher.objects.get(user=request.user)
                context = {
                    'form': form,
                    'form2': form2,
                    'profile_value': profile_value,
                }
            return render(request, 'profile.html', context)
        else:
            profile = current_user.student
            form2 = Student_profile_edit_form(request.POST, instance=profile)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                messages.success(request, 'Profile update successfully!')
                return redirect('profile')
            else:
                profile_value = Student.objects.get(user=request.user)
                context = {
                    'form': form,
                    'form2': form2,
                    'profile_value': profile_value,
                }
            return render(request, 'profile.html', context)
    else:
        current_user = User.objects.get(id=id)
        if current_user.is_depthead:
            profile = current_user.depthead
            form = Profile_edit_Form(instance=current_user)
            form2 = Depthead_profile_edit_form(instance=profile)
            profile_value = Depthead.objects.get(user=current_user)
            context = {
                'form': form,
                'form2': form2,
                'profile_value': profile_value
            }
        elif current_user.is_teacher:
            profile = current_user.teacher
            form = Profile_edit_Form(instance=current_user)
            form2 = Teacher_profile_edit_form(instance=profile)
            profile_value = Teacher.objects.get(user=current_user)
            context = {
                'form': form,
                'form2': form2,
                'profile_value': profile_value
            }
        elif current_user.is_student:
            profile = current_user.student
            form = Profile_edit_Form(instance=current_user)
            form2 = Student_profile_edit_form(instance=profile)
            profile_value = Student.objects.get(user=current_user)
            context = {
                'form': form,
                'form2': form2,
                'profile_value': profile_value
            }
    return render(request, 'profile.html', context)


@login_required
def password_change(request, id):
    if request.method == 'POST':
        current_user = User.objects.get(id=id)
        password_form = PasswordChangeForm(
            data=request.POST, user=current_user)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Password change successfully!')
            update_session_auth_hash(request, password_form.user)
            return redirect('profile')
        else:
            messages.warning(request, 'Try again!')
            if current_user.is_depthead:
                profile_value = Depthead.objects.get(user=current_user)
                val = 'password_change'
                context = {
                    'password_form': password_form,
                    'profile_value': profile_value,
                    'val': val,
                }
            elif current_user.is_teacher:
                profile_value = Teacher.objects.get(user=current_user)
                val = 'password_change'
                context = {
                    'password_form': password_form,
                    'profile_value': profile_value,
                    'val': val,
                }
            else:
                profile_value = Student.objects.get(user=current_user)
                val = 'password_change'
                context = {
                    'password_form': password_form,
                    'profile_value': profile_value,
                    'val': val,
                }
        return render(request, 'profile.html', context)
    else:
        current_user = User.objects.get(id=id)
        if current_user.is_depthead:
            profile_value = Depthead.objects.get(user=current_user)
            password_form = PasswordChangeForm(user=current_user)
            val = 'password_change'
            context = {
                'password_form': password_form,
                'profile_value': profile_value,
                'val': val,
            }
        elif current_user.is_teacher:
            profile_value = Teacher.objects.get(user=current_user)
            password_form = PasswordChangeForm(user=current_user)
            val = 'password_change'
            context = {
                'password_form': password_form,
                'profile_value': profile_value,
                'val': val,
            }
        elif current_user.is_student:
            profile_value = Student.objects.get(user=current_user)
            password_form = PasswordChangeForm(user=current_user)
            val = 'password_change'
            context = {
                'password_form': password_form,
                'profile_value': profile_value,
                'val': val,
            }
    return render(request, 'profile.html', context)
