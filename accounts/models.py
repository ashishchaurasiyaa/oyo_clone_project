from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

# Create your models here.

class HotalUser(User):
    profile_picture = models.ImageField(upload_to='profile', default='profile_pictures/default.png')
    phone_number = models.CharField(unique=True, max_length=12)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_varified = models.BooleanField(default=False)

    def send_otp(self):
        # Logic to send OTP to user via email/SMS
        pass

    def verify_otp(self, input_otp):
        return self.otp == input_otp

    class Meta:
        db_table = 'hotal_user'

class HotalVendor(User):
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(unique=True, max_length=12)
    profile_picture = models.ImageField(upload_to='profile', default='profile_pictures/default.png')
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_varified = models.BooleanField(default=False)

    class Meta:
        db_table = 'hotal_vendor'



class Amenities(models.Model):
    name = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='hotals')


class Hotal(models.Model):
    hotal_name = models.CharField(max_length=100)
    hotal_description = models.TextField()
    hotal_slug = models.SlugField(max_length=1000, unique=True)
    hotal_owner = models.ForeignKey(HotalVendor, on_delete=models.CASCADE, related_name='hotals')
    amenities = models.ManyToManyField(Amenities)
    hotal_price = models.FloatField()
    hotal_offer_price = models.FloatField()
    hotal_location = models.TextField()
    is_active = models.BooleanField(default=True)


class HotalImage(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='hotal_images')
    image = models.ImageField(upload_to='hotals')


class HotalManager(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='hotal_managers')
    manager_name = models.CharField(max_length=100)
    manager_contact = models.CharField(max_length=12)


class Booking(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_amount = models.FloatField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('canceled', 'Canceled')])

    def send_confirmation_email(self):
        # Send booking confirmation email
        subject = 'Booking Confirmation'
        message = f'Your booking for {self.hotal.hotal_name} is confirmed.'
        send_mail(subject, message, 'from@example.com', [self.user.email])

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])
    status = models.CharField(max_length=20, choices=[('successful', 'Successful'), ('failed', 'Failed'), ('pending', 'Pending')])

    def process_payment(self):
        # Implement payment processing logic here
        pass


class Review(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=1)  # You can set a range (1-5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Promotion(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='promotions')
    promotion_name = models.CharField(max_length=100)
    discount_percentage = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


class CustomerServiceInquiry(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='inquiries')
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='inquiries')
    inquiry_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)


class Room(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100)
    room_description = models.TextField()
    price_per_night = models.FloatField()
    amenities = models.ManyToManyField(Amenities)
    is_available = models.BooleanField(default=True)


class Wishlist(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='wishlists')
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class HotalPolicy(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='policies')
    policy_name = models.CharField(max_length=100)
    policy_description = models.TextField()
