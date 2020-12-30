from django.urls import path
from . import views,apiViews


urlpatterns = [
    path('depthead_dashboard/',views.depthead_home,name='depthead_dashboard'),
    path('users', views.users, name='users'),
    path('user_details/<int:id>', views.userdetails, name='userdetails'),
    path('allow_user/<int:id>', views.allow_user, name='allowuser'),
    path('student_info/', views.student_info, name='student_info'),
    path('teacher_info/', views.teacher_info, name='teacher_info'),
    path('course/', views.addcourse, name='course'),
    path('course_list', views.show_course, name='show_course'),
    path('savecourse', apiViews.save_course, name='savecourse'),
    #path('show_batch/', views.show_batch, name='show_batch'),
    path('results/', views.results, name='results'),
    path('results/<str:Dy_id>', views.batch_results, name='batch_results'),
    path('create_batch/', views.create_batch, name='create_batch'),
    path('batch_info/', views.find_batch, name='find_batch'),
    path('student_info/<str:Dy_id>/', views.batch_info, name='batch_info'),
    #path('results/<str:Dy_id>',views.batch_results, name='batch_results'),
    path('results/<str:Dy_id>/semester_01',views.semester_01, name='semester_01'),
    path('results/<str:Dy_id>/semester_02',views.semester_02, name='semester_02'),
    path('results/<str:Dy_id>/semester_03',views.semester_03, name='semester_03'),
    path('results/<str:Dy_id>/semester_04',views.semester_04, name='semester_04'),
    path('results/<str:Dy_id>/semester_05',views.semester_05, name='semester_05'),
    path('results/<str:Dy_id>/semester_06',views.semester_06, name='semester_06'),
    path('results/<str:Dy_id>/semester_07',views.semester_07, name='semester_07'),
    path('results/<str:Dy_id>/semester_08', views.semester_08, name='semester_08'),
]
