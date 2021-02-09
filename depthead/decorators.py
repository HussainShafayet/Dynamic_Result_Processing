from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.models import Student,Teacher

def login_required(function=None, redirect_field_name='Next', login_url='login'):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
""" Unauthenticated User decoratos """
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


""" Allowed_user by Group """
def allowed_user(allowed_roles=[]):
    def docorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            dept=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised user!')
        return wrapper_func
    return docorator
""" def student_required(function=None, login_required=True, redirect_field_name='depthead', login_url='home'):
    def is_shopkeeper(u):
        if login_required and not u.is_authenticated:
            return False
        return Student.objects.filter(user=u).exists()
    actual_decorator = user_passes_test(
        is_shopkeeper,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator """
