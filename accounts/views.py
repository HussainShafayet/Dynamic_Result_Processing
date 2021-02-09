from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
#User Reg,login and Logout
from .forms import (TeacherRegForm, StudentRegForm)
from .models import (User, Teacher, Student, Depthead)
from depthead.models import (Dept,Batch,Session)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (login, logout, authenticate,update_session_auth_hash)
from django.contrib.auth.models import (auth, Group)
#Reset Password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeForm)
#Accounts Activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
#Decorators
from depthead.decorators import unauthenticated_user

#My views here.
def home(request):
    return render(request, 'home.html')

#User Registration and Activation
@unauthenticated_user
def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherRegForm(request.POST, request.FILES)
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
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            val=1
            context = {
                'val':val
            }
            return render(request,'active_account.html',context)
        else:
            val='teacher_reg'
            context = {
                'form': form,
                'val':val,
            }
            return render(request, 'registration.html', context)
    else:
        form = TeacherRegForm()
        val='teacher_reg'
    context = {
            'form': form,
            'val': val
    }
    return render(request,'registration.html',context)
def ajax(request):
    if request.is_ajax():
        term=request.GET.get('term')
        dept = Dept.objects.all().filter(dept__icontains=term)
        response_content = list(dept.values())
        return JsonResponse(response_content, safe=False)


def ajax2(request):
    if request.is_ajax():
        term = request.GET.get('term')
        batch = Batch.objects.all().filter(batch__icontains=term)
        response_content = list(batch.values())
        return JsonResponse(response_content,safe=False)


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
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            val = 1
            context = {
                'val': val
            }
            return render(request, 'active_account.html', context)
        else:
            val='student_reg'
            context = {
                'form': form,
                'val': val,
            }
            return render(request, 'registration.html', context)
    else:
        form = StudentRegForm()
        val='student_reg'
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
        return render(request, 'active_account.html', {'val':2})
    else:
        return render(request, 'active_account.html')


#User Login and Logout

@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_depthead:
                    auth.login(request, user)
                    messages.success(request,'You are logged in!')
                    return redirect('depthead_dashboard')
                elif user.is_student:
                    auth.login(request, user)
                    return redirect('student_dashboard')
                elif user.is_teacher:
                    auth.login(request, user)
                    return redirect('teacher_dashboard')
                else:
                    auth.login(request, user)
                    messages.error(request, 'Your are not authorised user')
                    return redirect(home)
        else:
            conext = {
                'form': form
            }
            return render(request, 'login.html', conext)
    else:
        form = AuthenticationForm()
        conext = {
            'form':form
        }
        return render(request, 'login.html', conext)

def user_logout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('home')

#Reset Password
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


def profile(request):
    current_user = request.user
    if current_user.is_depthead:
        profile_value = Depthead.objects.get(user=current_user)
        user = User.objects.get(username=current_user)
        profile_details='profile_details'
        context = {
            'profile_value': profile_value,
            'user': user,
            'profile_details':profile_details
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
    elif current_user.is_teacher:
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


def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update success')
            return redirect('profile')
        else:
            messages.error(request, 'Try again')
            return redirect('edit-profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile-edit.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password change successfully!')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            messages.error(request, 'Try again')
            return redirect('password')
    else:
        current_user = request.user
        if current_user.is_depthead:
            profile_value=Depthead.objects.get(user=current_user)
            form = PasswordChangeForm(user=request.user)
            context = {
                'form': form,
                'profile_value':profile_value,
            }
        elif current_user.is_teacher:
            profile_value = Teacher.objects.get(user=current_user)
            form = PasswordChangeForm(user=request.user)
            context = {
                'form': form,
                'profile_value': profile_value,
            }
        elif current_user.is_student:
            profile_value = Student.objects.get(user=current_user)
            form = PasswordChangeForm(user=request.user)
            context = {
                'form': form,
                'profile_value': profile_value,
            }
    return render(request, 'profile.html', context)
