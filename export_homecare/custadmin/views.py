from django.shortcuts import render
from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
 # Import your Customer model
from django.shortcuts import redirect, get_object_or_404
from customerlogin.models import Customer;   
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
# Create your views here.

def index(request):
    return render(request, 'adminindex.html')
def displayuser(request):
    customers = Customer.objects.all()  
    print(customers)
    data_to_display = []
    for customer in customers:
          customer_data = {
       
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'gender': customer.gender,
            'phone': customer.phone1,
            'email': customer.email,
            'status': customer.status,
            'photo': customer.photo
        }
          data_to_display.append(customer_data)
    
    return render(request, 'displayuser.html', {'data_to_display': data_to_display})
  
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
 # Adjust this import based on your Customer model

def changeuserstatus(request, email):
    try:
        customer = Customer.objects.get(email=email)
        print(customer)
        if customer.status == '1':  # Assuming 1 means active and 0 means inactive
            customer.status = 0
            customer.save()
            messages.success(request, f'{customer.first_name} {customer.last_name}\'s account has been deactivated.')
        else:
            customer.status = 1
            customer.save()
            messages.success(request, f'{customer.first_name} {customer.last_name}\'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('displayuser')