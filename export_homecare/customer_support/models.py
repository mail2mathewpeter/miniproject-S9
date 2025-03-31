from django.db import models
from custadmin.models import Employee
# Create your models here.
class Policy(models.Model):
    Company_Policy = models.CharField(max_length=500)
    booking_rules = models.CharField(max_length=500)
    upload_document = models.CharField(max_length=500)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField() 
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.Company_Policy

