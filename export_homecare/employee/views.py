from django.shortcuts import render
from customerlogin.models import Customer,BookingDate,Booking; 
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
from django.shortcuts import render, get_object_or_404
from custadmin.models import Employee;  # Import your Customer model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index1(request):
    if request.session.get('login') == 'employee':
        id = request.session.get('id')
        
        # Get the employee instance
        employee = get_object_or_404(Employee, id=id)
        
        # Fetch employee's location
        employee_location = employee.designation
        
        # Fetch all pending bookings and filter by service provider location
        bookings = Booking.objects.filter(status="Unsolved")
        
        filtered_bookings = []
        total_amount = 0  # Initialize total amount

        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)

            # Filter based on service provider location
            if provider.Service_Provider_location == employee_location:
                # Fetch related BookingDate instances
                booking_dates = BookingDate.objects.filter(booking=booking)

                booking_data = {
                    'booking_id': booking.id,
                    'address': booking.address,
                    'notes': booking.notes,
                    'status': booking.status,
                    'service_provider_name': provider.service_provider_name,
                    'service_provider_email': provider.Service_Provider_Email,
                    'service_provider_gender': provider.Service_Provider_gender,
                    'Service_Provider_Experience': provider.Service_Provider_Experience,
                    'service_provider_phone': provider.Service_Provider_Phone,
                    'service_provider_location': provider.Service_Provider_location,
                    'service_name': service2.service_name,
                    'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                    'customer_email': booking.customer.email,
                    'customer_phone': booking.customer.phone1,
                    'dates_and_slots': [{'date': bd.service_start_date, 'slot': bd.time_slot} for bd in booking_dates]
                }
                
                filtered_bookings.append(booking_data)

        # Fetch solved bookings for the total amount calculation
        solved_bookings = Booking.objects.filter(
            Q(status="Solved"),
            service_provider__Service_Provider_location=employee.designation
        )

        # Calculate total amount from solved bookings
        total_amount = sum(int(booking.amount) for booking in solved_bookings)
        total_bookings_for_location = solved_bookings.count()
        total_customers = Customer.objects.filter(is_staff=False, is_superuser=False).count()

        # Render the template with the data
        return render(request, 'employeeindex.html', {
            'customer': employee,
            'id': id,
            'data_to_display': filtered_bookings,
            'total_amount': total_amount,
            'total_bookings_for_location': total_bookings_for_location,
            'total_customers':total_customers
        })
    else:
        return render(request, 'login1.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addservice1(request):
  if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
  
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'addserviceemployee.html',{'customer':employee,'id':id})
  else:
        return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def diplaychangepassword(request):
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'changepassword1.html',{'customer':employee,'id':id})

def editaccount1(request):
    
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
      # Get the logged-in user
    return render(request, 'editaccount1.html', {'customer': employee})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def employeccount1(request):
    if request.session.get('login') == 'employee':
     name=request.session.get('username')
     id=request.session.get('id')
     employee = get_object_or_404(Employee, id=id)
 # Get the logged-in user
     return render(request, 'accountview2.html', {'customer': employee})
    else:
     return render(request, 'login1.html')
    

def logout_view1(request):
    response = redirect('login1')  # Redirect to the login page
    response.set_cookie('loggedOut', 'true')
    return response

def addserviceprovider(request):
    
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
    services = service.objects.all()
    data_to_display1 = []
    for services in services:
          customer_data = {
            'service_name': services.service_name,
            'id': services.id,
          }
          data_to_display1.append(customer_data)
    return render(request, 'addserviceprovideremployee.html', {'data_to_display': data_to_display1,'customer':employee,'id':id})

# def index1(request,name):
#     return render(request, 'employeeindex.html',{'customer':name})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayuser1(request):
   if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
   
    employee = get_object_or_404(Employee, id=id)
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
        
    return render(request, 'displayuseremployee.html', {'data_to_display': data_to_display1,'customer':employee,'id':id})
   else:
        return render(request, 'login1.html')

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
            status="1"
            
             # You might want to hash this before saving
        )
        service1.save()
        
        messages.success(request, f'{service_name} has been successfully added.')
        return redirect('employee:displayservice')
        # Redirect to a success page
    else:
        return render(request, 'addserviceemployee.html')

from django.shortcuts import get_object_or_404, redirect

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayserviceproviderdata1(request):
   if request.session.get('login') == 'employee':
    service_providers = service_provider.objects.all()
    name=request.session.get('username')
    id=request.session.get('id')
    data_to_display1 = []
    employee = get_object_or_404(Employee, id=id)
 
    for provider in service_providers:
        # Fetch the related service instance
      services = get_object_or_404(service, id=provider.service_table)

        
      if employee.designation==provider.Service_Provider_location:
         k=provider.Service_Provider_location
         customer_data = {
            'id': provider.id,
            'service_name': provider.service_provider_name,
            'service_address': provider.Service_Provider_Address,
            'Service_Provider_Email': provider.Service_Provider_Email,
            'Service_Provider_Phone': provider.Service_Provider_Phone,
            'Service_Provider_gender': provider.Service_Provider_gender,
            'Service_Provider_Designation': services.service_name,
            'Service_Provider_service_id': provider.service_table,
            'Service_Provider_location': provider.Service_Provider_location,
            'Service_Provider_Experience': provider.Service_Provider_Experience,
            'Service_Provider_amountdefalult': provider.Service_Provider_amountdefalult,
            'photo': provider.photo,
            'Service_Provider_Id_proof': provider.Service_Provider_Id_proof,
            'Service_Provider_Qualification_Certificate': provider.Service_Provider_Qualification_Certificate,
            'status':provider.status,
        }

         data_to_display1.append(customer_data)

    return render(request, 'serviceproviderdisplay1.html', {'data_to_display': data_to_display1,'customer':employee,'id':id,'k':k})
   else:
        return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayservice(request):
   if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
    services = service.objects.all() 
    employee = get_object_or_404(Employee, id=id) 
    data_to_display1 = []
    for services in services:
          customer_data = {
              'id': services.id,
            'service_name': services.service_name,
            'service_description': services.service_description,
            'photo': services.photo,
            'status':services.status,
        }
          data_to_display1.append(customer_data)

        
    return render(request, 'displayserviceemployee.html', {'data_to_display': data_to_display1,'customer':employee,'id':id})
   else:
        return render(request, 'login1.html')
def send_otp_email_user_status(user_email,k,name):
  if k == 0:
    subject = 'Your Expert Homecare Account Activation Notice'
    message = f'Hello {name},\n\nWe are pleased to inform you that your Expert Homecare account has been activated as per your request.\n\nThank you for choosing Expert Homecare.\n\nBest regards,\nExpert Homecare Team'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
    

  elif k == 1:
        subject = 'Your Expert Homecare Account Deactivation Notice'
        message = f'Hello {name},\n\nWe regret to inform you that your Expert Homecare account has been deactivated due to suspicious activities detected. Please contact the Expert Homecare team to reactivate your account.\n\nThank you for your understanding.\n\nBest regards,\nExpert Homecare Team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

def changeuserstatus2(request, email):
    try:
        customer = Customer.objects.get(email=email)
        print(customer)
        
        if customer.status == '1':  # Assuming 1 means active and 0 means inactive
            customer.status = 0
            send_otp_email_user_status(email,customer.status,customer.first_name)

            customer.save()
            
            messages.success(request, f'{customer.first_name} {customer.last_name}\'s account has been deactivated.')
        else:
            customer.status = 1
            send_otp_email_user_status(email,customer.status,customer.first_name)
            customer.save()
            
            messages.success(request, f'{customer.first_name} {customer.last_name}\'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('employee:displayuser1')
# def deleteservice(request, id):
#     customer = get_object_or_404(service, id=id)
#     customer.delete()
#     return redirect('employee:displayservice') 
from django.urls import reverse
def delete_service(request, service_id):
    services = get_object_or_404(service, id=service_id)
    if services.status == '1':  # Assuming 1 means active and 0 means inactive
            services.status = '0'
            services.save()
            messages.success(request, f'{services.service_name}\'s account has been deactivated.')
    else:
            services.status = '1'
            services.save()
            messages.success(request, f'{services.service_name} \'s account has been activated.')
  
    services = service.objects.all()



  # Redirect to the service list view after deletion
    return redirect('employee:displayservice') 
    # return render(request, 'displayserviceemployee.html', {'data_to_display': services})
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def display_service(request):
  if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id) 
    services = service.objects.all()
    return render(request, 'displayserviceemployee.html', {'data_to_display': services,'customer': employee})
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def edit_service(request,service_id):
  if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
    services = get_object_or_404(service, id=service_id)
    
    return render(request, 'editservice.html',{'data_to_display': services, 'customer': employee})


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
    messages.success(request, f'{services.service_name}\'s  Updated Successfully.')

   
    return redirect('employee:displayservice') 
  # Redirect to the service list view after deletion
    # return redirect('employee:displayservice', {'data_to_display': services})
   
def addserviceproviderdata(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        service_provider_name = request.POST['name']
        Service_Provider_Address = request.POST['address']
        Service_Provider_Email = request.POST['email']
        Service_Provider_Phone = request.POST['phone']
        Service_Provider_gender = request.POST['gender']
        Service_Provider_Designation = request.POST['designation']
        Service_Provider_Experience = request.POST['experience']
        Service_Provider_amountdefalult = request.POST['amount']
        
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
            Service_Provider_location=employee.designation,
            Service_Provider_amountdefalult=Service_Provider_amountdefalult,
            service_table=service_instance.id,
            photo=f'images/{filename1}',             
            Service_Provider_Id_proof=f'images/{filename2}',
            Service_Provider_Qualification_Certificate=f'images/{filename3}',
            status="0",

             # You might want to hash this before saving
        )
        service1.save()
        send_otp_email_serviceprovider_joboffer(Service_Provider_Email,service_provider_name,Service_Provider_Designation)
        messages.success(request, f'{service_provider_name}\'s has been added Successfully.')
        return redirect('employee:displayserviceproviderdata1')
        # Redirect to a success page
    else:
        return render(request, 'addserviceprovideremployee.html')
    
def send_otp_email_serviceprovider_joboffer(Service_Provider_Email,service_provider_name,Service_Provider_Designation):
    services1 = get_object_or_404(service, id=Service_Provider_Designation)
    subject = 'Appointment Confirmation at ExpertHomeCare'
    message = f"""
Hello {service_provider_name},

We are thrilled to welcome you to the Expert Homecare family! Congratulations on being appointed as {services1.service_name} at Expert Homecare.

Your role is vital in our mission to provide top-quality care and services to our clients. We are confident that your skills and dedication will make a significant impact.

Thank you for choosing to be a part of our team. We look forward to your contributions and growth with us.
Using this link to Activate your account\n
'http://127.0.0.1:8000/customserviceprovider/serviceproviderpasswordadd/{Service_Provider_Email}/\n\n' 

Best regards,
The Expert Homecare Team
[9497036814]
[www.experthomecare.com]Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [Service_Provider_Email]
    send_mail(subject, message, from_email, recipient_list)

def changeserviceproviderstatus1(request, service_id):
    try:
        customer = service_provider.objects.get(id=service_id)
        print(customer)
        if customer.status == '4':  # Assuming 1 means active and 0 means inactive
            customer.status = '0'
            customer.save()
            messages.success(request, f'{customer.service_provider_name}\'s account has been deactivated.')
        elif customer.status=='0':
            customer.status = '4'
            customer.save()
            messages.success(request, f'{customer.service_provider_name} \'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('employee:displayserviceproviderdata1')

def editserviceproviderdata1(request,id2):
      if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(service_provider, id=id2)
        service_provider_name = request.POST['name']
        Service_Provider_Address = request.POST['address']
        Service_Provider_Email = request.POST['email']
        Service_Provider_Phone = request.POST['phone']
        Service_Provider_gender = request.POST['gender']
        Service_Provider_Designation = request.POST['designation']
        Service_Provider_Experience = request.POST['experience']
        Service_Provider_amountdefalult = request.POST['amount']
        file = request.FILES.get('file1', None)
        file2 = request.FILES.get('file2', None)
        file3 = request.FILES.get('file3', None)
        Service_Provider_Id_proof = request.FILES.get('file2', None) 
        Service_Provider_Qualification_Certificate = request.FILES.get('file3', None)  
        filename = None  
        filename1 = None  
        filename2 = None  
        if file:
                fs = FileSystemStorage(location=f'employee/static/images/')
                filename = fs.save(file.name, file)
                employee.photo = f'images/{filename}' 
        if Service_Provider_Id_proof:
                fs = FileSystemStorage(location=f'employee/static/images/')
                filename1 = fs.save(Service_Provider_Id_proof.name, file2)
                employee.Service_Provider_Id_proof = f'images/{filename1}' 
        if Service_Provider_Qualification_Certificate:
                fs = FileSystemStorage(location=f'employee/static/images/')
                filename2 = fs.save(Service_Provider_Qualification_Certificate.name, file3)
                employee.Service_Provider_Qualification_Certificate = f'images/{filename2}'
        employee.service_provider_name=service_provider_name
        employee.Service_Provider_Address=Service_Provider_Address
        employee.Service_Provider_Email=Service_Provider_Email
        employee.Service_Provider_Phone=Service_Provider_Phone
        employee.Service_Provider_gender=Service_Provider_gender
        employee.service_table=Service_Provider_Designation
        employee.Service_Provider_amountdefalult=Service_Provider_amountdefalult
        employee.Service_Provider_Experience=Service_Provider_Experience
        # Create a new customer record
        
        employee.save()
        messages.success(request, 'Service Provider Details Updated Sucessfully!')
        return redirect('employee:displayserviceproviderdata1')
      


def editemployeedata(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        print(name);
        print(id);
        employee = get_object_or_404(Employee, id=id)
        
        first_name = request.POST['first']
        last_name = request.POST['last']
        #gender = request.POST['gender']
       
        phone = request.POST['phone']

        experience = request.POST['experience']

        gender = request.POST.get('gender')
      
        file = request.FILES.get('file')
        filename = None  
        if file:
                fs = FileSystemStorage(location='customerlogin/static/images/')
                filename = fs.save(file.name, file)
                employee.photo = f'images/{filename}'


            # Update the customer record
    
        employee.name = first_name
        employee.address = last_name
        employee.gender = gender
        employee.phone = phone
      
        employee.experience = experience
       
        employee.save()

        messages.success(request, 'Your profile details has been updated successfully!')
        return redirect('employee:employeccount1')  # Redirect to a success page
   
   
    return render(request, 'editaccount1.html', {'customer': employee})

def updatepassword1(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        password = request.POST['password']
       

            # Update the customer record
        
        employee.password = password
        
       
        employee.save()

        messages.success(request, 'Your account password has been updated successfully!')
        return redirect('employee:employeccount1') # Redirect to a success page
    
@cache_control(no_cache=True, no_store=True, must_revalidate=True)   
def displayserviceproviderdataeditpage(request,id1):
  if request.session.get('login') == 'employee':
    name=request.session.get('username')
    id=request.session.get('id')
    data_to_display1 = []
    data_to_display = []
    
    employee = get_object_or_404(Employee, id=id)
    serviceprovider_id = get_object_or_404(service_provider, id=id1)
    services1=serviceprovider_id.service_table;
 
    servicename1 = get_object_or_404(service, id=services1)
    

        # Fetch the related service instance
    services = service.objects.all()  
   
    for services in services:
          customer_data = {
            'service_name': services.service_name,
            'id': services.id,
          }
          data_to_display.append(customer_data)
    print(serviceprovider_id.Service_Provider_location);
    print(employee.designation);
    if employee.designation==serviceprovider_id.Service_Provider_location:
          customer_data = {
            'id': serviceprovider_id.id,
            'service_name': serviceprovider_id.service_provider_name,
            'service_address': serviceprovider_id.Service_Provider_Address,
            'Service_Provider_Email': serviceprovider_id.Service_Provider_Email,
            'Service_Provider_Phone': serviceprovider_id.Service_Provider_Phone,
            'Service_Provider_gender': serviceprovider_id.Service_Provider_gender,
            'Service_Provider_Designation': servicename1.service_name,
             'Service_Provider_service_id': serviceprovider_id.service_table,
             'Service_Provider_amountdefalult':serviceprovider_id.Service_Provider_amountdefalult,
            # 'Service_Provider_location': serviceprovider_id.Service_Provider_location,
            'Service_Provider_Experience': serviceprovider_id.Service_Provider_Experience,
            'photo': serviceprovider_id.photo,
            'Service_Provider_Id_proof': serviceprovider_id.Service_Provider_Id_proof,
            'Service_Provider_Qualification_Certificate': serviceprovider_id.Service_Provider_Qualification_Certificate,
            'status':serviceprovider_id.status,
        }

          data_to_display1.append(customer_data)

    return render(request, 'serviceprovideredit.html', {'service_provider': data_to_display1,'service': data_to_display,'customer':employee,'id':id})
  else:
     return render(request, 'login1.html')

def logoutaemployee(request):
   
    request.session['login'] = " "
    
    
    # Redirect to a success page or login page
    return redirect('login1')

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def validate_email1(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if email already exists in the database
        if service_provider.objects.filter(Service_Provider_Email=email).exists():
            data = {
                'valid': False,
                'message': 'Email already exists.'
            }
        else:
            data = {
                'valid': True,
                'message': 'Email is available.'
            }
        
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



from django.shortcuts import render, get_object_or_404


@cache_control(no_cache=True, no_store=True, must_revalidate=True)  
def viewbookingall(request):
      if request.session.get('login') == 'employee':
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        
        # Fetch employee's location
        employee_location = employee.designation
        
        # Fetch all pending bookings
        bookings = Booking.objects.filter(status="pending")
        
        filtered_bookings = []
        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)
            
            # Filter based on service provider location
            if provider.Service_Provider_location == employee_location:
                # Fetch related BookingDate instances
                booking_dates = BookingDate.objects.filter(booking=booking)
                
                booking_data = {
                    'booking_id': booking.id,
                    'address': booking.address,
                    'notes': booking.notes,
                    'status': booking.status,
                    'amount': booking.amount,
                    'payment': booking.paymentstatus,
                    'service_provider_name': provider.service_provider_name,
                    'service_provider_email': provider.Service_Provider_Email,
                    'service_provider_gender': provider.Service_Provider_gender,
                    'Service_Provider_Experience': provider.Service_Provider_Experience,
                    'service_provider_phone': provider.Service_Provider_Phone,
                    'service_provider_location': provider.Service_Provider_location,
                    'service_name': service2.service_name,
                    'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                    'customer_email': booking.customer.email,
                    'customer_phone': booking.customer.phone1,
                    'dates_and_slots': [{'date': bd.service_start_date, 'slot': bd.time_slot} for bd in booking_dates]
                }
                
                filtered_bookings.append(booking_data)
                return render(request, 'viewbooking.html', {'data_to_display': filtered_bookings, 'customer': employee, 'id': id})
        else:
          return render(request, 'login1.html')
        
@cache_control(no_cache=True, no_store=True, must_revalidate=True)  
def viewbooking(request):
      if request.session.get('login') == 'employee':
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        
        # Fetch employee's location
        employee_location = employee.designation
        
        # Fetch all pending bookings
        bookings = Booking.objects.filter().order_by('-id')
        
        filtered_bookings = []
        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)
            
            # Filter based on service provider location
            if provider.Service_Provider_location == employee_location:
                # Fetch related BookingDate instances
                booking_dates = BookingDate.objects.filter(booking=booking)
                
                booking_data = {
                    'booking_id': booking.id,
                    'address': booking.address,
                    'notes': booking.notes,
                    'status': booking.status,
                    'amount': booking.amount,
                    'payment': booking.paymentstatus,
                    'service_provider_name': provider.service_provider_name,
                    'service_provider_email': provider.Service_Provider_Email,
                    'service_provider_gender': provider.Service_Provider_gender,
                    'Service_Provider_Experience': provider.Service_Provider_Experience,
                    'service_provider_phone': provider.Service_Provider_Phone,
                    'service_provider_location': provider.Service_Provider_location,
                    'service_name': service2.service_name,
                    'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                    'customer_email': booking.customer.email,
                    'customer_phone': booking.customer.phone1,
                    'dates_and_slots': [{'date': bd.service_start_date, 'slot': bd.time_slot} for bd in booking_dates]
                }
                
                filtered_bookings.append(booking_data)
                print(filtered_bookings)
        return render(request, 'viewbooking.html', {'data_to_display': filtered_bookings, 'customer': employee, 'id': id})
      else:
         return render(request, 'login1.html')
def changebookingstatus(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'GET':
        booking.status="Solved"
        booking.save()

        messages.success(request, 'Booked Service has been successfully Solved.')
        return redirect('employee:viewbooking')  # Replace with the URL where you want to redirect after deletion
    
    
# views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import numpy as np
# import cv2
# from django.core.files.uploadedfile import InMemoryUploadedFile
# import os
# from django.conf import settings
# from django.core.files.storage import default_storage

# # Load Haar Cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# @csrf_exempt
# def validate_image(request):
#     if request.method == 'POST' and 'file1' in request.FILES:
#         # Get the uploaded file
#         uploaded_file: InMemoryUploadedFile = request.FILES['file1']
#         file_name = uploaded_file.name  # Get the original file name

#         # Convert the uploaded file to an image
#         file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
#         img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
#         if img is None:
#             return JsonResponse({"status": "error", "message": "Unable to read the image."})

#         # Convert the image to grayscale (required for Haar Cascade)
#         gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # Detect faces in the image
#         faces = face_cascade.detectMultiScale(
#             gray_img, 
#             scaleFactor=1.2, 
#             minNeighbors=6, 
#             minSize=(50, 50)
#         )

#         # Save the image with detected faces

#         output_image_path = os.path.join(settings.BASE_DIR, 'static', 'media', uploaded_file.name)  # Save to the media directory
#         if len(faces) > 0:
#             # Draw rectangles around the detected faces
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
#             # Save the image to the media directory
#             default_storage.save('detected_faces.jpg', uploaded_file)
#             cv2.imwrite(output_image_path, img)

#             # Construct the URL for the image
#             image_url = os.path.join( '/static', 'media', uploaded_file.name)


#             return JsonResponse({
#                 "status": "success",
#                 "message": f"Detected {len(faces)} face(s) in the image.",
#                 "image_url": image_url,
#                 "file_name": file_name
#             })
#         else:
#             default_storage.save('detected_faces.jpg', uploaded_file)
#             cv2.imwrite(output_image_path, img)
#             image_url = os.path.join( '/static', 'media', uploaded_file.name)

#             return JsonResponse({"status": "error", "message": "No human face detected in the image.",
#                                    "image_url": image_url,})

#     return JsonResponse({"status": "error", "message": "Invalid request."})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
  # Adjust model imports as needed
@cache_control(no_cache=True, no_store=True, must_revalidate=True)  
def serviceproviderpdfemployee(request):
    if request.session.get('login') == 'employee':
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        
        # Fetch employee's location (assuming it's stored in a field named 'location')
        employee_location = employee.designation  # Adjust this based on your actual field name

        # Filter service providers based on employee's location
        service_providers = service_provider.objects.filter(Service_Provider_location=employee_location)

        providers_data = []
        for provider in service_providers:
            # Fetch associated service object
            service_obj = get_object_or_404(service, id=provider.service_table)  # Adjust 'service_id' based on your actual foreign key field

            provider_data = {
                'service_provider_name': provider.service_provider_name,
                'Service_Provider_Email': provider.Service_Provider_Email,
                'Service_Provider_Phone': provider.Service_Provider_Phone,
                'Service_Provider_Address': provider.Service_Provider_Address,
                'Service_Provider_gender': provider.Service_Provider_gender,
                'Service_Provider_Experience': provider.Service_Provider_Experience,
                'Service_Provider_location': provider.Service_Provider_location,
                'photo': provider.photo,
                'service_name': service_obj.service_name,
            }
            providers_data.append(provider_data)

        # Prepare the context
        context = {
            'service_providers': providers_data,
            'current_year': timezone.now().year
        }

        return render(request, 'serviceproviderpdf.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)  
def viewbookingpdfemployee(request):
    if request.session.get('login') == 'employee':
        # Get the logged-in employee's ID from the session
        emp_id = request.session.get('id')
        employee = get_object_or_404(Employee, id=emp_id)
        
        # Fetch employee's location (assuming it's stored in a field named 'designation')
        employee_location = employee.designation  # Adjust this based on your actual field name

        # Filter service providers based on the employee's location
        service_providers = service_provider.objects.filter(Service_Provider_location=employee_location)

        providers_data = []
        for provider in service_providers:
            # Fetch associated service object
            service_obj = get_object_or_404(service, id=provider.service_table)  # Adjust 'service_table' based on your actual foreign key field

            # Fetch bookings associated with this service provider
            bookings = Booking.objects.filter(service_provider=provider)

            # Prepare booking details
            booking_data = [
                {
                    'id': booking.id,
                    'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                    'address': booking.address,
                    'booking_date': booking.booking_date.date(),  # Show only the date
                    'amount': booking.amount,
                    'status': booking.status,
                    'service_provider_name': provider.service_provider_name,
                    'photo': provider.photo.url if provider.photo else None, 

                }
                for booking in bookings
            ]

            provider_data = {
                'service_provider_name': provider.service_provider_name,
                'Service_Provider_Email': provider.Service_Provider_Email,
                'Service_Provider_Phone': provider.Service_Provider_Phone,
                'Service_Provider_Address': provider.Service_Provider_Address,
                'Service_Provider_gender': provider.Service_Provider_gender,
                'Service_Provider_Experience': provider.Service_Provider_Experience,
                'Service_Provider_location': provider.Service_Provider_location,
                'photo': provider.photo.url if provider.photo else None,  # Handle photo URL correctly
                'service_name': service_obj.service_name,
                'bookings': booking_data,  # Include booking details
            }
            providers_data.append(provider_data)

        # Prepare the context
        context = {
            'service_providers': providers_data,
            'current_year': timezone.now().year,
        }

        return render(request, 'viewbookingpdfemployee.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')