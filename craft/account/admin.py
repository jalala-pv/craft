from django.contrib import admin
from .models import Productss,Orders,DeliveryAddress

# Register your models here.

admin.site.register(Productss)
admin.site.register(Orders)
admin.site.register(DeliveryAddress)