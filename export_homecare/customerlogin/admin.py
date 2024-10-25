from django.contrib import admin

# Register your models here.
from .models import Customer,Booking,BookingDate,Message

admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(BookingDate)
admin.site.register(Message)