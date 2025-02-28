from django.shortcuts import render
from manager.forms  import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from hr.forms import *
import csv
from django.core.mail import send_mail
from student.models import *
import random

# Create your views here.

def hr_login_required(func):
    def inner(request, *args, **kwargs):
        hrun = request.session.get('hruser')
        if hrun:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('hr_login'))
    return inner

def hr_home(request):
    un = request.session.get('hruser')
    if un:
        UO = User.objects.get(username=un)
        d = {'UO': UO}
    return render(request, 'hr/hr_home.html')

def hr_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_staff:
            EO = EmployeeProfile.objects.get(username=AUO)
            if EO.role == 'HR':
                login(request, AUO)
                request.session['hruser'] = un
                return HttpResponseRedirect(reverse('hr_home'))
            return HttpResponse('Not a HR')
        return HttpResponse('invalid creds')
    return render(request, 'hr/hr_login.html')

@hr_login_required
def hr_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('hr_home'))

@hr_login_required
def students_rating(request):
    std_ratings = Rating.objects.all()
    d = {'std_ratings': std_ratings}
    return render(request, 'hr/students_rating.html', d)

def hr_un(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        UO = User.objects.get(username=un)
        EO = EmployeeProfile.objects.get(username=UO)
        if UO and UO.is_active:
            if UO.is_staff and EO.role == 'HR':
                otp = random.randint(1000, 9999)
                request.session['otp'] = otp
                request.session['hruser'] = un
                email = UO.email
                message = f"Your OTP for forgot password is: {otp}"
                send_mail(
                    'OTP For Forgot password',
                    message,
                    'deepankarmali2001@gmail.com',
                    [email],
                    fail_silently=False
                )
                return HttpResponseRedirect(reverse('hr_otp'))
            return HttpResponse('Not a HR')
        return HttpResponse('Invalid Username')
    return render(request, 'hr/hr_un.html')

def hr_otp(request):
    if request.method == 'POST':
        uotp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(uotp) == gotp:
            return HttpResponseRedirect(reverse('hr_change_pw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'hr/hr_otp.html')


def hr_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('hruser')
            UO = User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('hr_login'))
    return render(request, 'hr/hr_change_pw.html')


@hr_login_required
def schedule_mock(request):
    hrun = request.session.get('hruser')
    UO = User.objects.get(username=hrun)
    PO = EmployeeProfile.objects.get(username=UO)
    ESFO = SchedulingForm()
    d = {'ESFO': ESFO}
    if request.method == 'POST' and request.FILES:
        SFDO = SchedulingForm(request.POST, request.FILES)
        if SFDO.is_valid():
            SFDO.save()
            with open(r"C:\Users\Deepankar Mali\Desktop\Book1.csv", 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                usernames = [i[1]+i[2] for i in csv_reader]
                print(usernames)
                for un in usernames:    
                    SO = User.objects.get(username=un)
                    if SO:
                        email = SO.email
                        print(email)
                        name = f"{SO.first_name} {SO.last_name}"
                        message = f"""
Dear {name},

I hope you're doing well! We are excited to invite you for a mock interview as part of your preparation for the  at QSpiders. This session is designed to help you practice and receive constructive feedback before your official interview.

Interview Details:
📅 Date: {SFDO.cleaned_data.get('date')}
⏰ Time: {SFDO.cleaned_data.get('time')}
📍 Location/Platform: QSpiders Bhubaneswar
⏳ Duration: 30min

During the mock interview, we will focus on {SFDO.cleaned_data.get('subject')}, followed by a feedback session.

Please confirm your availability at your earliest convenience. Feel free to reach out if you have any questions. We look forward to helping you prepare!

Best regards,
{SO.first_name} {SO.last_name}
{PO.role}
Qspiders
{PO.pno}"""
        
                        send_mail(
                            f"Subject: Invitation for Mock Interview -  QSpiders Bhubaneswar",
                            message,
                            'deepankarmali2001@gmail.com',
                            [email],
                            fail_silently=False
                        )   
                        send_mail(
                            ""
                        )                                                                                      
            return HttpResponseRedirect(reverse('hr_home'))
        return HttpResponse('Invalid Data')
  
    return render(request, 'hr/schedule_mock.html', d)