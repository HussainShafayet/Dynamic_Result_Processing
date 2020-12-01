from django.urls import path
from . import views

urlpatterns = [
    path('teacher_dasboard/',views.teacher_dashboard,name='teacher_dashboard'),
]
