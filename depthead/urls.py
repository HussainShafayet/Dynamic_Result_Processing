from django.urls import path
from . import views,apiViews


urlpatterns = [
    path('depthead_dashboard/',views.depthead_home,name='depthead_dashboard'),
    path('users', views.users, name='users'),
    path('user_details/<int:id>', views.userdetails, name='userdetails'),
    path('allow_user/<int:id>', views.allow_user, name='allowuser'),
    path('student_info/', views.student_info, name='student_info'),
    path('teacher_info/', views.teacher_info, name='teacher_info'),
    path('course/', views.course, name='course'),
    path('course_list', views.show_course, name='show_course'),
    path('savecourse', apiViews.save_course, name='savecourse'),
    path('create_batch/',views.createbatch,name='create_batch'),
    path('show_batch/',views.show_batch,name='show_batch'),
]
