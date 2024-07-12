from django.shortcuts import render
from customerlogin.models import Customer; 
from .models import service;
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

from custadmin.models import Employee;  # Import your Customer model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
# Create your views here.
def index1(request):
    return render(request, 'employeeindex.html')
def addservice1(request):
    return render(request, 'addserviceemployee.html')

# def index1(request,name):
#     return render(request, 'employeeindex.html',{'customer':name})


def displayuser1(request):
    customers = Customer.objects.all()  
    print(customers)
    data_to_display1 = []
    for customer in customers:
       if customer.status != '2':
          customer_data = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'gender': customer.gender,
            'phone': customer.phone1,
            'email': customer.email,
            'status': customer.status,
            'photo': customer.photo,
        }
          data_to_display1.append(customer_data)
       else:
        # Do nothing or handle the case where status is 2 if necessary
          pass
        
    return render(request, 'displayuseremployee.html', {'data_to_display': data_to_display1})


def addservicesubmit(request):
    if request.method == 'POST':
        service_name = request.POST['service_name']
        description1 = request.POST['description']
        file = request.FILES.get('file1', None)       
        fs = FileSystemStorage(location=f'employee/static/images/')
        filename = fs.save(file.name, file)
 
        # Create a new customer record
        service1 = service(
            service_name=service_name,
            service_description=description1,
            photo=f'images/{filename}',
             # You might want to hash this before saving
        )
        service1.save()
        
      
        return redirect('employee:displayservice')
        # Redirect to a success page
    else:
        return render(request, 'addserviceemployee.html')

def displayservice(request):
    services = service.objects.all()  
    print(services)
    data_to_display1 = []
    for services in services:
          customer_data = {
              'id': services.id,
            'service_name': services.service_name,
            'service_description': services.service_description,
            'photo': services.photo,
        }
          data_to_display1.append(customer_data)

        
    return render(request, 'displayserviceemployee.html', {'data_to_display': data_to_display1})

from django.shortcuts import get_object_or_404, redirect
# def deleteservice(request, id):
#     customer = get_object_or_404(service, id=id)
#     customer.delete()
#     return redirect('employee:displayservice') 

def delete_service(request, id):
    services = get_object_or_404(service, id=id)
    k=services.service_name
    services.delete()
   
    messages.success(request, f"{services.service_name} "'Service deleted successfully.')
    services = service.objects.all()
  # Redirect to the service list view after deletion
    return render(request, 'displayserviceemployee.html', {'data_to_display': services})
def display_service(request):
    services = service.objects.all()
    return render(request, 'displayserviceemployee.html', {'data_to_display': services})

def edit_service(request,id):
    services = get_object_or_404(service, id=id)
    
    return render(request, 'editservice.html',{'data_to_display': services})