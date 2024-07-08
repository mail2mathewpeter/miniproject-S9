from django.db import models

# Create your models here.


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
 

    def __str__(self):
        return self.name
