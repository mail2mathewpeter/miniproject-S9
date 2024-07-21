from django.db import models

# Create your models here.
class service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
       return self.service_name
class service_provider(models.Model):
    service_provider_name = models.CharField(max_length=100)
    Service_Provider_Address = models.CharField(max_length=100)
    Service_Provider_Email = models.CharField(max_length=100)
    Service_Provider_Phone = models.CharField(max_length=100)
    Service_Provider_gender = models.CharField(max_length=10,blank=True,null=True)
    service_table= models.IntegerField()
    Service_Provider_Experience = models.CharField(max_length=100)
    Service_Provider_Id_proof = models.FileField(upload_to='images/')
    photo = models.ImageField(upload_to='images/')
    Service_Provider_Qualification_Certificate = models.FileField(upload_to='images/')
    status = models.CharField(max_length=100)
    password = models.CharField(max_length=1000,blank=True,null=True)
    
    def __str__(self):
       return self.service_provider_name

