from django.db import models

# Create your models here.
class service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
       return self.service_name
