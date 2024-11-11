from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
import random

class HotalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile', default='profile_pictures/default.png')
    phone_number = models.CharField(unique=True, max_length=12)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'hotal_user'

    def __str__(self):
        return self.user.username

    def send_otp(self):
        self.otp = str(random.randint(100000, 999999))  # Generate a random OTP
        # Logic to send OTP to user via email/SMS (Placeholder)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {self.otp}',
            'ashishkumar.mailto@gmail.com',
            [self.user.email],
        )
        self.save()

    def verify_otp(self, input_otp):
        return self.otp == input_otp

    def save(self, *args, **kwargs):
        if not self.phone_number.isdigit() or len(self.phone_number) != 12:
            raise ValueError("Phone number must be 12 digits.")
        super().save(*args, **kwargs)


class HotalVendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(unique=True, max_length=12)
    profile_picture = models.ImageField(upload_to='profile', default='profile_pictures/default.png')
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'hotal_vendor'

    def __str__(self):
        return self.business_name


class Amenities(models.Model):
    name = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='amenities')

    def __str__(self) -> str:
        return self.name

class SubAmenity(models.Model):
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE, related_name='sub_amenities')
    name = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='sub_amenities', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} (Sub-Amenity of {self.amenity.name})"

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

    def __str__(self):
        return self.hotal_name


class HotalImage(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='hotal_images')
    image = models.ImageField(upload_to='hotals')


class HotalManager(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='hotal_managers')
    manager_name = models.CharField(max_length=100)
    manager_contact = models.CharField(max_length=12)

    def __str__(self):
        return self.manager_name

class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'

    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_amount = models.FloatField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONFIRMED)

    def __str__(self):
        return f'Booking for {self.hotal.hotal_name} by {self.user.user.username}'

    def send_confirmation_email(self):
        subject = 'Booking Confirmation'
        message = f'Your booking for {self.hotal.hotal_name} is confirmed.'
        send_mail(subject, message, 'ashishkumar.mailto@gmail.com', [self.user.email])

    def process_payment(self, payment_method):
        if payment_method not in ['credit_card', 'paypal', 'cash']:
            raise ValueError("Unsupported payment method.")
        self.status = Booking.Status.CONFIRMED
        self.save()

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])
    status = models.CharField(max_length=20, choices=[('successful', 'Successful'), ('failed', 'Failed'), ('pending', 'Pending')])

    def process_payment(self):
        pass


class Review(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=1)  # You can set a range (1-5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.hotal.hotal_name} by {self.user.user.username}'

class Promotion(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='promotions')
    promotion_name = models.CharField(max_length=100)
    discount_percentage = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.promotion_name

class CustomerServiceInquiry(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='inquiries')
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='inquiries')
    inquiry_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Inquiry by {self.user.user.username} for {self.hotal.hotal_name}'

class Room(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100)
    room_description = models.TextField()
    price_per_night = models.FloatField()
    amenities = models.ManyToManyField(Amenities)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.room_type} in {self.hotal.hotal_name}'

class Wishlist(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='wishlists')
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Wishlist for {self.user.user.username}'

class Notification(models.Model):
    user = models.ForeignKey(HotalUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.user.username}'

class HotalPolicy(models.Model):
    hotal = models.ForeignKey(Hotal, on_delete=models.CASCADE, related_name='policies')
    policy_name = models.CharField(max_length=100)
    policy_description = models.TextField()

    def __str__(self):
        return self.policy_name