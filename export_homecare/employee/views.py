from django.shortcuts import render
from customerlogin.models import Customer; 
from .models import service,service_provider;
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

def addserviceprovider(request):
    services = service.objects.all()
    data_to_display1 = []
    for services in services:
          customer_data = {
            'service_name': services.service_name,
            'id': services.id,
          }
          data_to_display1.append(customer_data)
    return render(request, 'addserviceprovideremployee.html', {'data_to_display': data_to_display1})

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

from django.shortcuts import get_object_or_404, redirect


def displayserviceproviderdata1(request):
    service_providers = service_provider.objects.all()
    data_to_display1 = []

    for provider in service_providers:
        # Fetch the related service instance
        services = get_object_or_404(service, id=provider.service_table)
       
        customer_data = {
            'id': provider.id,
            'service_name': provider.service_provider_name,
            'service_address': provider.Service_Provider_Address,
            'Service_Provider_Email': provider.Service_Provider_Email,
            'Service_Provider_Phone': provider.Service_Provider_Phone,
            'Service_Provider_gender': provider.Service_Provider_gender,
            'Service_Provider_Designation': services.service_name,
            'Service_Provider_Experience': provider.Service_Provider_Experience,
            'photo': provider.photo,
            'Service_Provider_Id_proof': provider.Service_Provider_Id_proof,
            'Service_Provider_Qualification_Certificate': provider.Service_Provider_Qualification_Certificate,
            'status':provider.status,
        }

        data_to_display1.append(customer_data)

    return render(request, 'serviceproviderdisplay1.html', {'data_to_display': data_to_display1})
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


# def deleteservice(request, id):
#     customer = get_object_or_404(service, id=id)
#     customer.delete()
#     return redirect('employee:displayservice') 
from django.urls import reverse
def delete_service(request, service_id):
    services = get_object_or_404(service, id=service_id)
   
    services.delete()
   
    messages.success(request, f"{services.service_name} "'Service deleted successfully.')
    services = service.objects.all()
  # Redirect to the service list view after deletion
    return redirect('employee:displayservice') 
    # return render(request, 'displayserviceemployee.html', {'data_to_display': services})
def display_service(request):
    services = service.objects.all()
    return render(request, 'displayserviceemployee.html', {'data_to_display': services})

def edit_service(request,service_id):
    services = get_object_or_404(service, id=service_id)
    
    return render(request, 'editservice.html',{'data_to_display': services})


def updateservicedata(request,service_id):
   
    services = get_object_or_404(service, id=service_id)
    service_name = request.POST['service_name']
    description = request.POST['description']
    file = request.FILES.get('file1')
    filename = None  
    if file:
                fs = FileSystemStorage(location=f'employee/static/images/')
                filename = fs.save(file.name, file)
                services.photo = f'images/{filename}'


            # Update the customer record
    
    services.service_name = service_name
    services.service_description = description
    services.save()
    messages.success(request, 'Service Updated Successfully')
   
    return redirect('employee:displayservice') 
  # Redirect to the service list view after deletion
    # return redirect('employee:displayservice', {'data_to_display': services})
   
def addserviceproviderdata(request):
    if request.method == 'POST':
        service_provider_name = request.POST['name']
        Service_Provider_Address = request.POST['address']
        Service_Provider_Email = request.POST['email']
        Service_Provider_Phone = request.POST['phone']
        Service_Provider_gender = request.POST['gender']
        Service_Provider_Designation = request.POST['designation']
        Service_Provider_Experience = request.POST['experience']
        photo = request.FILES.get('file1', None)   
        Service_Provider_Id_proof = request.FILES.get('file2', None) 
        Service_Provider_Qualification_Certificate = request.FILES.get('file3', None)     
        fs = FileSystemStorage(location=f'employee/static/images/')
        filename1 = fs.save(photo.name, photo)
        filename2 = fs.save(Service_Provider_Id_proof.name, Service_Provider_Id_proof)
        filename3 = fs.save(Service_Provider_Qualification_Certificate.name, Service_Provider_Qualification_Certificate)
        
        service_instance = get_object_or_404(service, id=int(Service_Provider_Designation))
        # Create a new customer record
        service1 = service_provider(
            service_provider_name=service_provider_name,
            Service_Provider_Address=Service_Provider_Address,
            Service_Provider_Email=Service_Provider_Email,
            Service_Provider_Phone=Service_Provider_Phone,
            Service_Provider_gender=Service_Provider_gender,
            Service_Provider_Experience=Service_Provider_Experience,
            service_table=service_instance.id,
            photo=f'images/{filename1}',             
            Service_Provider_Id_proof=f'images/{filename2}',
            Service_Provider_Qualification_Certificate=f'images/{filename3}',
            status="0",

             # You might want to hash this before saving
        )
        service1.save()
        return redirect('employee:displayserviceproviderdata1')
        # Redirect to a success page
    else:
        return render(request, 'addserviceprovideremployee.html')
    

def changeserviceproviderstatus1(request, service_id):
    try:
        customer = service_provider.objects.get(id=service_id)
        print(customer)
        if customer.status == '1':  # Assuming 1 means active and 0 means inactive
            customer.status = '0'
            customer.save()
            messages.success(request, f'{customer.service_provider_name}\'s account has been deactivated.')
        else:
            customer.status = '1'
            customer.save()
            messages.success(request, f'{customer.service_provider_name} \'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('employee:displayserviceproviderdata1')
