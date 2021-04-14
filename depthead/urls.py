from django.urls import path
from . import views, apiViews
#from .views import Users
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.depthead_home, name='depthead_dashboard'),
    path('users', views.users, name='users'),
    path('user_search/', csrf_exempt(views.search), name='search'),
    path('student_search/', csrf_exempt(views.student_search), name='student_search'),
    path('teacher_search/', csrf_exempt(views.teacher_search), name='teacher_search'),
    path('user_details/<int:id>', views.userdetails, name='userdetails'),
    path('allow_user/<int:id>', views.allow_user, name='allowuser'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('student_info', views.student_info, name='student_info'),
    path('teacher_info', views.teacher_info, name='teacher_info'),
    path('add_syllabus', views.add_syllabus, name='add_syllabus'),
    path('syllabus', views.view_syllabus, name='syllabus'),
    path('syllabus/<str:syllabus_id>',views.syllabus_semester, name='syllabus_semester'),
    path('syllabus/<str:syllabus_id>/<str:semester>/views_course_list', views.view_course_list_all, name='view_course_list'),
    path('syllabus/<str:syllabus_id>/<str:semester>/add_course',views.add_course, name='add_course'),
    path('savecourse', apiViews.save_course, name='savecourse'),
    path('delete_course/<str:syllabus_id>/<str:semester>/<int:id>',views.delete_course, name='delete_course'),
    #path('results/', views.results, name='results'),
    #path('results/<str:Dy_id>', views.batch_results, name='batch_results'),
    path('create_batch/', views.create_batch, name='create_batch'),
    path('batch_info/', views.find_batch, name='find_batch'),
    path('batch_info/<str:batch>/',views.batch_info, name='batch_info'),
    path('batch_info/<str:batch>/<str:semester>/result_info',views.result_info, name='result_info'),
    path('batch_info/<str:batch>/<str:semester>/result_info/<str:course>',views.course_result_details, name='course_result_details'),
    path('save_paper_code', apiViews.save_paper_code, name='save_paper_code'),
    path('re-add/', views.re_admission, name='re-add'),
    #path('results/<str:Dy_id>',views.batch_results, name='batch_results'),
    #path('results/<str:Dy_id>/semester_01',views.semester_01, name='semester_01'),
    #path('results/<str:Dy_id>/semester_02',views.semester_02, name='semester_02'),
    #path('results/<str:Dy_id>/semester_03',views.semester_03, name='semester_03'),
    #path('results/<str:Dy_id>/semester_04',views.semester_04, name='semester_04'),
    #path('results/<str:Dy_id>/semester_05',views.semester_05, name='semester_05'),
    #path('results/<str:Dy_id>/semester_06',views.semester_06, name='semester_06'),
    #path('results/<str:Dy_id>/semester_07',views.semester_07, name='semester_07'),
    #path('results/<str:Dy_id>/semester_08',views.semester_08, name='semester_08'),
]
