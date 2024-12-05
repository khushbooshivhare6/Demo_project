# my_email_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),  
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:pk>/', views.update_student, name='update_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('view/', views.student_list, name='student_list'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('verify_password/', views.verify_password, name='verify_password'),
    path('login/',views.login,name='login'),

    
]
