# Generated by Django 5.1.2 on 2024-11-05 03:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Amenities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1000)),
                ("icon", models.ImageField(upload_to="amenities")),
            ],
        ),
        migrations.CreateModel(
            name="Hotal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hotal_name", models.CharField(max_length=100)),
                ("hotal_description", models.TextField()),
                ("hotal_slug", models.SlugField(max_length=1000, unique=True)),
                ("hotal_price", models.FloatField()),
                ("hotal_offer_price", models.FloatField()),
                ("hotal_location", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("amenities", models.ManyToManyField(to="accounts.amenities")),
            ],
        ),
        migrations.CreateModel(
            name="HotalImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="hotals")),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotal_images",
                        to="accounts.hotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HotalManager",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("manager_name", models.CharField(max_length=100)),
                ("manager_contact", models.CharField(max_length=12)),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotal_managers",
                        to="accounts.hotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HotalPolicy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("policy_name", models.CharField(max_length=100)),
                ("policy_description", models.TextField()),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="policies",
                        to="accounts.hotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HotalUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        default="profile_pictures/default.png", upload_to="profile"
                    ),
                ),
                ("phone_number", models.CharField(max_length=12, unique=True)),
                (
                    "email_token",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("otp", models.CharField(blank=True, max_length=10, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "hotal_user",
            },
        ),
        migrations.CreateModel(
            name="CustomerServiceInquiry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("inquiry_type", models.CharField(max_length=100)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("response", models.TextField(blank=True, null=True)),
                ("response_date", models.DateTimeField(blank=True, null=True)),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inquiries",
                        to="accounts.hotal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inquiries",
                        to="accounts.hotaluser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_in_date", models.DateField()),
                ("check_out_date", models.DateField()),
                ("number_of_guests", models.PositiveIntegerField()),
                ("total_amount", models.FloatField()),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("confirmed", "Confirmed"), ("canceled", "Canceled")],
                        default="confirmed",
                        max_length=20,
                    ),
                ),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="accounts.hotal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="accounts.hotaluser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HotalVendor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("business_name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=12, unique=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        default="profile_pictures/default.png", upload_to="profile"
                    ),
                ),
                (
                    "email_token",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("otp", models.CharField(blank=True, max_length=10, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "hotal_vendor",
            },
        ),
        migrations.AddField(
            model_name="hotal",
            name="hotal_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotals",
                to="accounts.hotalvendor",
            ),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="accounts.hotaluser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("paypal", "PayPal"),
                            ("cash", "Cash"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("successful", "Successful"),
                            ("failed", "Failed"),
                            ("pending", "Pending"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="accounts.booking",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Promotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("promotion_name", models.CharField(max_length=100)),
                ("discount_percentage", models.FloatField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="promotions",
                        to="accounts.hotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.PositiveIntegerField(default=1)),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="accounts.hotal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="accounts.hotaluser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("room_type", models.CharField(max_length=100)),
                ("room_description", models.TextField()),
                ("price_per_night", models.FloatField()),
                ("is_available", models.BooleanField(default=True)),
                ("amenities", models.ManyToManyField(to="accounts.amenities")),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="accounts.hotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubAmenity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1000)),
                (
                    "icon",
                    models.ImageField(blank=True, null=True, upload_to="sub_amenities"),
                ),
                (
                    "amenity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_amenities",
                        to="accounts.amenities",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hotal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlists",
                        to="accounts.hotal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlists",
                        to="accounts.hotaluser",
                    ),
                ),
            ],
        ),
    ]
