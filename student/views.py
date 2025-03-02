from django.shortcuts import render
from student.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import csv
import random
from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required



# Create your views here.

def login_required(func):
    def inner(request, *args, **kwargs):
        un = request.session.get('username')
        if un:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('student_login'))
    return inner

def student_home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        PO = StudentProfile.objects.get(username=UO)
        d = {'UO': UO, 'PO': PO}
        return render(request, 'student/student_home.html', d)
    return render(request, 'student/student_home.html')

def student_register(request):
    ESUF = StudentUserForm()
    ESPF = StudentProfileForm()
    d = {'ESUF': ESUF, 'ESPF': ESPF}
    if request.method == 'POST' and request.FILES:
        SUFDO = StudentUserForm(request.POST)
        SPFDO = StudentProfileForm(request.POST, request.FILES)
        if SUFDO.is_valid() and SPFDO.is_valid():
            pw = SUFDO.cleaned_data.get('password')
            MSUFDO = SUFDO.save(commit=False)
            MSUFDO.set_password(pw)
            MSUFDO.save()
            MSPFDO = SPFDO.save(commit=False)
            MSPFDO.username = MSUFDO
            MSPFDO.save()
            return HttpResponseRedirect(reverse('student_login'))
        return HttpResponse('invalid data')

    # with open(r"C:\Users\Deepankar Mali\Desktop\Book1.csv", mode='r') as file:
    #     csv_reader = csv.reader(file)
    #     next(csv_reader)
    #     for i in (csv_reader):
    #         UO = User(first_name = i[1], last_name = i[2], email = i[4], username = i[1]+i[2])
    #         UO.set_password(i[1])
    #         UO.save()
    #         PO = StudentProfile(username=UO, phone = i[3], add = i[6], course = i[5])
    #         PO.save()
    #     return HttpResponse('done')
    return render(request, 'student/student_register.html', d)

def student_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('student_home'))
        return HttpResponse('Invalid Creds')
    return render(request, 'student/student_login.html')

@login_required
def student_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('student_home'))


def student_un(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        UO = User.objects.get(username=un)
        if UO and UO.is_active:
            if UO.is_staff or UO.is_superuser:
                return HttpResponse('Invalid Username')
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['username'] = un
            email = UO.email
            message = f"Your OTP for forgot password is: {otp}"
            send_mail(
                'OTP For Forgot password',
                message,
                'deepankarmali2001@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('student_otp'))
        return HttpResponse('Invalid Username')
    return render(request, 'student/student_un.html')

def student_otp(request):
    if request.method == 'POST':
        uotp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(uotp) == gotp:
            return HttpResponseRedirect(reverse('student_change_pw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'student/student_otp.html')


def student_change_pw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('student_login'))
    return render(request, 'student/student_change_pw.html')


@login_required
def display_mock_ratings(request):
    un = request.session.get('username')
    SO = User.objects.get(username=un)
    d = {'SO': SO}
    return render(request, 'student/display_mock_ratings.html', d)