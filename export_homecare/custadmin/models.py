from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password, check_password as django_check_password

class Employee(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Storing hashed password directly

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    def __str__(self):
        return self.email
# Define Employee model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,blank=True,null=True)
    designation = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=100)
    password = models.CharField(max_length=1000,blank=True,null=True)
 

    def __str__(self):
        return self.name
