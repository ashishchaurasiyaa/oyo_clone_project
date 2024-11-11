from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HotalUser, HotalVendor, Hotal, Amenities, HotalImage, SubAmenity
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail, generateSlug
import random
import logging

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotal_user = HotalUser.objects.filter(email=email)

        if not hotal_user.exists():
            messages.warning(request, 'User does not exist')
            return redirect('/accounts/login/')
        if not hotal_user[0].is_varified:
            messages.warning(request, 'Please verify your email address')
            return redirect('/accounts/login/')

        hotal_user = authenticate(username=hotal_user[0].username, password=password)
        if hotal_user:
            messages.success(request, 'Login Successful')
            login(request, hotal_user)
            return redirect('/accounts/dashboard/')
        messages.warning(request, 'Invalid Credentials')
        return redirect('/accounts/login/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/accounts/login/')

def about_us(request):
    return render(request,'about_us.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        hotal_user = HotalUser.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotal_user.exists():
            messages.warning(request, 'User already exists')
            return redirect('/accounts/register/')

        hotal_user = HotalUser.objects.create(
            username=email,
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


def verify_email_token(request, token):
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
        messages.warning(request, 'User does not exist')
        return redirect('/accounts/login/')

    otp = random.randint(1000, 9999)
    hotal_user.update(otp=otp)
    sendOTPtoEmail(email, otp)
    return redirect(f'/accounts/verify_otp/{email}/')


def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotal_user = HotalUser.objects.get(email=email)

        if otp == hotal_user.otp:
            messages.success(request, 'OTP verified successfully')
            login(request, hotal_user)
            return redirect('/accounts/dashboard/')
        messages.warning(request, 'Invalid OTP')
        return redirect(f'/accounts/verify_otp/{email}/')
    return render(request, 'verify_otp.html')


def login_vendor(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotal_vendor = HotalVendor.objects.filter(email=email)

        if not hotal_vendor.exists():
            messages.warning(request, 'Vendor does not exist')
            return redirect('/accounts/vendor/login-vendor/')
        if not hotal_vendor[0].is_varified:
            messages.warning(request, 'Please verify your email address')
            return redirect('/accounts/vendor/login-vendor/')

        vendor_user = authenticate(username=hotal_vendor[0].username, password=password)
        if vendor_user:
            messages.success(request, 'Login Successful')
            login(request, vendor_user)
            return redirect('/accounts/dashboard/')
        messages.warning(request, 'Invalid Credentials')
        return redirect('/accounts/vendor/login-vendor/')
    return render(request, 'vendor/login-vendor.html')


def register_vendor(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        business_name = request.POST.get('business_name')

        hotal_vendor = HotalVendor.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotal_vendor.exists():
            messages.warning(request, 'Vendor already exists')
            return redirect('/accounts/vendor/register-vendor/')

        hotal_vendor = HotalVendor.objects.create(
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken(),
            business_name=business_name
        )
        hotal_vendor.set_password(password)
        hotal_vendor.save()
        sendEmailToken(email, hotal_vendor.email_token)
        messages.success(request, 'Email sent to your email address')
        return redirect('/accounts/vendor/register-vendor/')
    return render(request, 'vendor/register_vendor.html')


@login_required(login_url='login_vendor')
def dashboard(request):
    hotels = Hotal.objects.filter(hotal_owner=request.user)
    context = {'hotels': hotels}
    return render(request, 'vendor/vendor_dashboard.html', context)


@login_required(login_url='login_vendor')
def add_hotal(request):
    if request.method == 'POST':
        hotal_name = request.POST.get('hotal_name')
        hotal_description = request.POST.get('hotal_description')
        amenities = request.POST.getlist('amenities')
        sub_amenities = request.POST.getlist('sub_amenities')  # Added for sub-amenities
        hotal_price = request.POST.get('hotal_price')
        hotal_offer_price = request.POST.get('hotal_offer_price')
        hotal_location = request.POST.get('hotal_location')
        hotal_slug = generateSlug(hotal_name)

        try:
            hotal_vendor = HotalVendor.objects.get(user=request.user)
        except HotalVendor.DoesNotExist:
            messages.error(request, 'No associated vendor account found. Please contact support or log in again.')
            return redirect('login_vendor')

        if not hotal_name or not hotal_description or not hotal_price or float(hotal_price) < 0:
            messages.error(request, 'Please fill all required fields correctly.')
            return redirect('/accounts/add_hotal/')

        hotal = Hotal.objects.create(
            hotal_name=hotal_name,
            hotal_description=hotal_description,
            hotal_price=hotal_price,
            hotal_offer_price=hotal_offer_price,
            hotal_location=hotal_location,
            hotal_owner=hotal_vendor,
            hotal_slug=hotal_slug
        )

        for amenity_id in amenities:
            try:
                amenity = Amenities.objects.get(id=amenity_id)
                hotal.amenities.add(amenity)
            except Amenities.DoesNotExist:
                messages.warning(request, f'Amenity with ID {amenity_id} does not exist.')

        for sub_amenity_id in sub_amenities:
            try:
                sub_amenity = SubAmenity.objects.get(id=sub_amenity_id)
                hotal.sub_amenities.add(sub_amenity)
            except SubAmenity.DoesNotExist:
                messages.warning(request, f'Sub-Amenity with ID {sub_amenity_id} does not exist.')

        messages.success(request, 'Hotal added successfully')
        return redirect('/accounts/dashboard/')

    amenities = Amenities.objects.all()
    return render(request, 'vendor/add_hotal.html', context={'amenities': amenities})


def get_sub_amenities(request, amenity_id):
    amenity = get_object_or_404(Amenities, id=amenity_id)
    sub_amenities = SubAmenity.objects.filter(amenity_id=amenity_id).values('id', 'name')
    return JsonResponse({'sub_amenities': list(sub_amenities)})


@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotal.objects.get(hotal_slug=slug)
    if request.method == "POST":
        image = request.FILES['image']
        HotalImage.objects.create(hotal=hotel_obj, image=image)
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_images.html', context={'images': hotel_obj.hotal_images.all()})


@login_required(login_url='login_vendor')
def delete_image(request, id):
    hotal_image = HotalImage.objects.get(id=id)
    hotal_image.delete()
    messages.success(request, "Hotal Image Deleted")
    return redirect('/account/dashboard/')
