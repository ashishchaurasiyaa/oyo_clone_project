from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(HotalUser)
admin.site.register(HotalVendor)
admin.site.register(Amenities)
admin.site.register(SubAmenity)