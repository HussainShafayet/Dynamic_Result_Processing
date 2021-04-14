from django.urls import path
from . import views, apiViews


urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('assign_course/', views.assign_course, name='assign_course'),
    path('completed_courses/', views.completed_courses, name='completed_courses'),
    path('assign_course/<str:batch>/<str:course>/course_result/', views.course_result, name='course_result'),
    path('completed_courses/<str:batch>/<str:course>/archived_course/',views.archived_course, name='archived_courses'),
    path('exam_khata/', views.exam_khata, name='exam_khata'),
    path('exam_khata/<str:batch>/<str:course>/',views.assaigned_khatas, name='assigned_khatas'),
    path('saveresult_theory', apiViews.save_result_theory, name='saverusult_theory'),
    path('saveresult_sessional', apiViews.save_result_sessional, name='saverusult_sessional'),
    path('saveresult_exam_part', apiViews.save_result_Exam_Part, name='exam_part'),
    path('assign_course/<str:batch>/<str:course>/course_result/result_submit', views.result_submit, name='result_submit'),
    path('assign_course/<str:batch>/<str:course>/course_result/delete_student/<int:id>', views.delete_student, name='delete_student'),
    
]
