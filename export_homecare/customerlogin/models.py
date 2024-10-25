from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from employee.models import service,service_provider;  

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10,blank=True,null=True)
    phone1 = models.CharField(max_length=15)
    address = models.CharField(max_length=50,blank=True,null=True)
    photo = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True,blank=True,null=True)
    status = models.CharField(max_length=30,default='0')
    is_staff = models.BooleanField(default=False)
    
    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    

class Booking(models.Model):
    service_provider = models.ForeignKey(service_provider, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    address=models.CharField(max_length=100)
    booking_date = models.DateTimeField()
    paymentstatus = models.CharField(max_length=100,blank=True, null=True)
    amount = models.CharField(max_length=100,blank=True, null=True);
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30)
    

    def __str__(self):
           return self.address
class BookingDate(models.Model):
 
    booking = models.ForeignKey(Booking, related_name='booking_dates', on_delete=models.CASCADE)
    service_start_date = models.DateField()
    time_slot = models.CharField(max_length=10, default='FULL_DAY')

    def __str__(self):
        return f"Service Date: {self.service_start_date} for Booking ID: {self.booking.id}"
    
    from django.db import models

class Chat(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"
    
class Message(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'