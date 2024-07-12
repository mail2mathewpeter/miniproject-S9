# from django.contrib.auth.backends import BaseBackend
# from .models import Customer

# class EmailBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None,status=1 **kwargs):
#         try:
#             user = Customer.objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except Customer.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Customer.objects.get(pk=user_id)
#         except Customer.DoesNotExist:
#             return None

# accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Customer

from custadmin.models import Employee

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        
        try:
            # Check if the user exists in the Customer model and has status='1'
            customer = Customer.objects.get(email=email, status='1')
            if customer.check_password(password):
                return customer
            
            # Check if the user exists in the Employee model and has status='2'
            employee = Employee.objects.get(email=email, status='2')
            if employee.check_password(password):
                return employee
            
        except Customer.DoesNotExist:
            pass  # Continue to check Employee
        except Employee.DoesNotExist:
            pass  # User doesn't exist in both models or doesn't match status
        
        return "Failed"  # Authentication failed

