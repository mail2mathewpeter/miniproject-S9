from django.contrib import admin

# Register your models here.
from .models import Employee,payments

admin.site.register(Employee)
admin.site.register(payments)