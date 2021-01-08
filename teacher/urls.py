from django.urls import path
from . import views,apiViews


urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assign_course/', views.assign_course, name='assign_course'),
    path('assign_course_details/<str:batch>/<str:course>', views.details_course, name='assign_course_details'),
    path('assign_course_result/', views.assign_course_result, name='assign_course_result'),
    path('course_result/<str:batch>/<str:course>', views.course_result, name='course_result'),
    path('course_result', views.course_result, name='course_result_GET'),
    path('saveresult', apiViews.save_result, name='saverusult'),
]
