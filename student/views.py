from django.shortcuts import render

# My views here.
def student_dashboard(request):
    return render(request,'user_dashboard.html')