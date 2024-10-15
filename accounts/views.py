from math import frexp

from PIL.ImagePalette import random
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import HotalUser
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken
import random
from .utils import sendOTPtoEmail


# Create your views here.
def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotal_user = HotalUser.objects.filter(
            email = email)

        if not hotal_user.exists():
            messages.warning(request, 'User does not exists')
            return redirect('/accounts/login/')
        if not hotal_user[0].is_varified:
            messages.warning(request, 'Please verify your email address')
            return redirect('/accounts/login/')

        hotal_user = authenticate(username=hotal_user[0].username, password=password)
        if hotal_user:
            messages.success(request, 'Login Successful')
            login(request, hotal_user)
            return redirect('/accounts/login/')
        messages.warning(request, 'Invalid Credentials')
        return redirect('/accounts/login/')
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email =request.POST.get('email')
        phone_number =request.POST.get('phone_number')
        password =request.POST.get('password')

        hotal_user = HotalUser.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        )

        if hotal_user.exists():
            messages.warning(request, 'User already exists')
            return redirect('/accounts/register/')

        hotal_user = HotalUser.objects.create(
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken()
        )
        hotal_user.set_password(password)
        hotal_user.save()
        sendEmailToken(email, hotal_user.email_token)

        messages.success(request, 'Email sent to your email address')
        return redirect('/accounts/register/')

    return render(request, 'register.html')


def verify_email_token(request,token):
    try:
        hotal_user = HotalUser.objects.get(email_token=token)
        hotal_user.is_varified = True
        hotal_user.save()
        messages.success(request, 'Email verified successfully')
        return redirect('/accounts/login/')
    except HotalUser.DoesNotExist:
        messages.warning(request, 'Invalid Token')
        return redirect('/accounts/login/')


def send_otp(request, email):
    hotal_user = HotalUser.objects.filter(email=email)
    if not hotal_user.exists():
        messages.warning(request,'User does not exists')
        return redirect('/accounts/login/')

    otp = random.randint(1000,9999)
    hotal_user.update(otp=otp)
    sendOTPtoEmail(email,otp)
    return redirect(f'/accounts/verify_otp/{email}/')

def verify_otp(request,email):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotal_user = HotalUser.objects.get(email=email)

        if otp == hotal_user.otp:
            message.success(request, 'OTP verified successfully')
            login(request, hotal_user)
            return redirect('/accounts/login/')
        messages.warning(request, 'Invalid OTP')
        return redirect(f'/accounts/verify_otp/{email}/')

    return render(request, 'verify_otp.html')