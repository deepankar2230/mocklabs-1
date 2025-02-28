from django.shortcuts import render
from django.shortcuts import render
from manager.forms  import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from trainer.forms import *
from student.models import *
import random
from django.core.mail import send_mail

# Create your views here.

def trainer_login_required(func):
    def inner(request, *args, **kwargs):
        tun = request.session.get('traineruser')
        if tun:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('trainer_login'))
    return inner     

def trainer_home(request):
    return render(request, 'trainer/trainer_home.html')

def trainer_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_staff:
            EO = EmployeeProfile.objects.get(username=AUO)
            if EO.role == 'Trainer':
                login(request, AUO)
                request.session['traineruser'] = un
                return HttpResponseRedirect(reverse('trainer_home'))
            return HttpResponse('Not a Trainer')
        return HttpResponse('invalid creds')
    return render(request, 'trainer/trainer_login.html')


@trainer_login_required
def trainer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('trainer_home'))


def trainer_un(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        UO = User.objects.get(username=un)
        EO = EmployeeProfile.objects.get(username=UO)
        if UO and UO.is_active and UO.is_staff and EO.role == 'Trainer':
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['traineruser'] = un
            email = UO.email
            message = f"Your OTP for forgot password is: {otp}"
            send_mail(
                'OTP For Forgot password',
                message,
                'deepankarmali2001@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('trainer_otp'))
        return HttpResponse('Invalid Username')
    return render(request, 'trainer/trainer_un.html')

def trainer_otp(request):
    if request.method == 'POST':
        uotp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(uotp) == gotp:
            return HttpResponseRedirect(reverse('trainer_change_pw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'trainer/trainer_otp.html')


def trainer_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('traineruser')
            UO = User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('trainer_login'))
    return render(request, 'trainer/trainer_change_pw.html')



@trainer_login_required
def mock(request):
    ERO = RatingForms()
    std_profile = StudentProfile.objects.all()
    d = {'ERF': ERO, 'std_profile':std_profile}
    if request.method == 'POST':
        student_name = request.POST.get('student')  
        rating_data = RatingForms(request.POST)
        if rating_data.is_valid():
            trainer = request.session.get('traineruser')
            trainer_obj = User.objects.get(username=trainer) 
            mut_rating_data = rating_data.save(commit=False)
            mut_rating_data.conducted_by = trainer_obj
            
            # get student object
            std_obj = User.objects.get(username=student_name) 
            mut_rating_data.student = std_obj
            mut_rating_data.save()
            return HttpResponseRedirect(reverse('mock'))
        

    return render(request, 'trainer/mock.html', d)