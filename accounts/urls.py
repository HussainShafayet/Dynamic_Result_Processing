from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('teacher_registration',views.teacher_registration, name='teacher_registration'),
    path('student_registration', views.student_registration, name='student_registration'),
    path('depthead_registration', views.depthead_registraion, name='depthead_registration'),
    path('ajax/', views.ajax, name='ajax'),
    path('ajax2/', views.ajax2, name='ajax2'),
    path('ajax3/', views.ajax3, name='ajax3'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login',views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('password_reset/', views.ResetPassword.as_view(), name='password_reset'),
    path('password_reset/done/', views.ResetPasswordDone.as_view(),name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.ResetPasswordConfirm.as_view(),name='password_reset_confirm'),
    path('reset/done/', views.ResetPasswordComplete.as_view(), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit-profile/<int:id>', views.profile_edit, name='edit_profile'),
    path('profile/change-password/<int:id>', views.password_change, name='password'),
]
