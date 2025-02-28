from django.urls  import path
from hr.views import *

urlpatterns = [
    path('hr_login', hr_login, name='hr_login'),
    path('hr_home', hr_home, name='hr_home'),
    path('hr_logout', hr_logout, name='hr_logout'),
    path('hr_un/', hr_un, name='hr_un'),
    path('hr_otp/', hr_otp, name='hr_otp'),
    path('hr_change_pw/', hr_change_pw, name='hr_change_pw'),
    path('students_rating/', students_rating, name='students_rating'),
    path('schedule_mock/', schedule_mock, name='schedule_mock'),
]

