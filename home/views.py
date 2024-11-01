from xxlimited_35 import error

from django.contrib.messages import success
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


# Create your views here.

def index(request):
    return render(request, 'index.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
        elif '@' not in email:
            messages.error(request, 'Enter a valid email address.')
        else:
            try:
                send_mail(
                    f"Contact form submission from {name}",
                    message,
                    email,
                    ['ashishkumar.mailto@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Thank you for reaching out to us. We will get back to you soon.")
            except Exception as e:
                messages.error(request, "There was an error while submitting the form. Please try again.")

    return render(request, 'contact.html')
