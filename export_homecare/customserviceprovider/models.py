from django.db import models
from customerlogin.models import Booking,Customer
from employee.models import service_provider
# Create your models here.
class Accessoriesbuy(models.Model):
    Booking1 = models.ForeignKey(Booking, on_delete=models.CASCADE)
    Additionalaccessoriesamount=models.CharField(max_length=100)
    proofupdate= models.ImageField(upload_to='images/')
    update_date = models.DateTimeField()
    def __str__(self):
           return self.Additionalaccessoriesamount
    
class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    serviceprovider = models.ForeignKey(service_provider, on_delete=models.CASCADE)  # Foreign key to CustomerDetails
    service_received = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    experience = models.TextField()
    suggestions = models.TextField(blank=True)  # Optional suggestions for improvement
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"Feedback from {self.customer.first_name} - Rating: {self.rating}"
    
