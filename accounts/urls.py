from django.urls import path
from . import views

urlpatterns = [
    # User Authentication
    path('login/', views.login_page, name='login'),
    path('logout/',views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('about-us/', views.about_us, name='about_us'),
    path('send_otp/<email>/', views.send_otp, name='send_otp'),
    path('verify_otp/<email>/', views.verify_otp, name='verify_otp'),
    path('verify-account/<str:token>/', views.verify_email_token, name='verify_email_token'),

    # Vendor Authentication
    path('login-vendor/', views.login_vendor, name='login_vendor'),
    path('register-vendor/', views.register_vendor, name='register_vendor'),

    # Vendor Dashboard and Hotel Management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_hotal/', views.add_hotal, name='add_hotal'),

    # Amenities and Images
    path('get-sub-amenities/<int:amenity_id>/', views.get_sub_amenities, name='get_sub_amenities'),
    path('upload_images/<slug:slug>/', views.upload_images, name='upload_images'),
    path('delete_image/<int:id>/', views.delete_image, name="delete_image"),
]
