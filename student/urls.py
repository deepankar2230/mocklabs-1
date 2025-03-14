from django.urls import path
from student.views import *

urlpatterns = [
    path('student_home/', student_home, name='student_home'),
    path('student_register/', student_register, name='student_register'),
    path('student_login/', student_login, name='student_login'),
    path('student_logout/', student_logout, name='student_logout'),
    path('student_un/', student_un, name='student_un'),
    path('student_otp/', student_otp, name='student_otp'),
    path('student_change_pw/', student_change_pw, name='student_change_pw'),
    path('display_mock_ratings/', display_mock_ratings, name='display_mock_ratings')
]