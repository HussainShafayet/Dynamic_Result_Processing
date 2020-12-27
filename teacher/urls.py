from django.urls import path
from . import views,apiViews


urlpatterns = [
    path('teacher_dashboard/', views.teacher_profile, name='teacher_dashboard'),
    path('teacher_dashboard/<str:Dy_id>',views.course_result, name='course_result'),
    path('course_result', views.course_result, name='course_result_GET'),
    path('saveresult', apiViews.save_result, name='saverusult'),
]
