from django.urls import path
from . import views

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_results/',views.student_result,name='student_result')
]
