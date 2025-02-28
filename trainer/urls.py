from django.urls  import path
from trainer.views import *

urlpatterns = [
    path('trainer_login', trainer_login, name='trainer_login'),
    path('trainer_home', trainer_home, name='trainer_home'),
    path('trainer_logout', trainer_logout, name='trainer_logout'),
    path('trainer_un/', trainer_un, name='trainer_un'),
    path('trainer_otp/', trainer_otp, name='trainer_otp'),
    path('trainer_change_pw/', trainer_change_pw, name='trainer_change_pw'),
    path('mock', mock, name='mock'),
]

