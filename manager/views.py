from django.shortcuts import render
from manager.forms import *
import random
import string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


# Create your views here.

def login_required(func):
    def inner(request, *args, **kwargs):
        un = request.session.get('username')
        if un:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('manager_login'))
    return inner

def manager_home(request):
    return render(request, 'manager/manager_home.html')

def manager_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_staff:
            if AUO.is_superuser:
                login(request, AUO)
                request.session['username'] = un
                return HttpResponseRedirect(reverse('manager_home'))
            return HttpResponse('not an admin')
        return HttpResponse('Invalid Creds')
    return render(request, 'manager/manager_login.html')

@login_required
def manager_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('manager_login'))

def add_employee(request):
    un = request.session.get('username')
    if un:
        EEUFO = EmployeeUserForm()
        EEPFO = EmployeeProfileForm()
        d = {'EEUFO': EEUFO, 'EEPFO': EEPFO}
        if request.method == 'POST':
            EUFDO = EmployeeUserForm(request.POST)
            EPFDO = EmployeeProfileForm(request.POST)
            if EUFDO.is_valid() and EPFDO.is_valid():
                un = f"{(EUFDO.cleaned_data.get('first_name').lower())}{EPFDO.cleaned_data.get('pno')[-4:]}"
                pw = ''.join([random.choice(string.ascii_letters) for i in range(1, 6)])
                MEUFDO = EUFDO.save(commit=False)
                MEUFDO.username = un
                MEUFDO.set_password(pw)
                MEUFDO.is_staff = True
                MEUFDO.save()
                MEPFDO = EPFDO.save(commit=False)
                MEPFDO.username = MEUFDO
                MEPFDO.save()
                message = f"""Hello dear {MEUFDO.first_name} {MEUFDO.last_name}

Your Username Password is mentioned below, please login with these credentials.
                            
Username = {un}
Password = {pw}
                            
Regards
QSpiders/JSpiders/Pyspiders"""
                email = MEUFDO.email
                send_mail(
                    f'Thanks for Registration {MEUFDO.first_name}',
                    message,
                    'deepankarmali2001@gmail.com',
                    [email],
                    fail_silently=False
                )
                print(un)
                print(pw)
                return HttpResponse('done')
            return HttpResponse('invalid data')
        return render(request, 'manager/add_employee.html', d)
    return HttpResponseRedirect(reverse('manager_login'))