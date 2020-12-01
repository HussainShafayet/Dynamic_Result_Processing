from django.shortcuts import render

# Create your views here.


def teacher_dashboard(request):
    return render(request, 'user_dashboard.html',{'val':'user_t'})
