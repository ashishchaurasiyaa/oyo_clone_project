from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('send_otp/<email>/', views.send_otp, name='send_otp'),
    path('verify-otp/<email>/', views.verify_otp, name='verify_otp'),
    path('verify-account/<str:token>/', views.verify_email_token, name='verify_email_token'),
    path('login-vendor/', views.login_vendor, name='login_vendor'),
    path('register-vendor/', views.register_vendor, name='register_vendor'),
    path('dashboard/', views.dashboard, name="dashboard"),

]
