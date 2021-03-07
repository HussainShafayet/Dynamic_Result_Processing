from django.urls import path
from . import views, apiViews


urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assign_course/', views.assign_course, name='assign_course'),
    path('assigned_courses/', views.assigned_courses, name='assigned_courses'),
    path('assign_course/<str:batch>/<str:course>/course_result/', views.course_result, name='course_result'),
    path('assigned_courses/<str:batch>/<str:course>/course_result2/', views.course_result2, name='course_result2'),
    path('exam_khata/', views.exam_khata, name='exam_khata'),
    path('exam_khata/<str:batch>/<str:course>/', views.assaigned_khatas, name='assigned_khatas'),
    path('saveresult_theory', apiViews.save_result_theory, name='saverusult_theory'),
    path('saveresult_sessional', apiViews.save_result_sessional, name='saverusult_sessional'),
    path('assign_course/<str:batch>/<str:course>/course_result/calculate_course_gpa',views.calculate_course_GPA, name='calculate_course_gpa'),
    path('assign_course/<str:batch>/<str:course>/course_result/result_submit', views.result_submit, name='result_submit'),
    path('assign_course/<str:batch>/<str:course>/course_result/delete_student/<int:id>', views.delete_student, name='delete_student'),
    
    #path('assign_course_details/<str:batch>/<str:course>', views.details_course, name='assign_course_details'),
    #path('assign_course_result/', views.assign_course_result, name='assign_course_result'),
    #path('course_result/<str:batch>/<str:course>', views.course_result, name='course_result'),
    #path('course_result', views.course_result, name='course_result_GET'),
    
]
