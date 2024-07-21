from django.contrib import admin
from .models import service
from .models import service_provider
# Register your models here.
admin.site.register(service)
admin.site.register(service_provider)