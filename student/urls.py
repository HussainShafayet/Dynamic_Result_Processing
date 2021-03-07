from django.urls import path
from . import views

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('active_courses/', views.active_courses, name='active_courses'),
    path('student_results/<str:semester>',views.student_result,name='student_result')
]
