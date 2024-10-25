from django.shortcuts import render
from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.db.models import Sum 
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from customerlogin.models import Booking,BookingDate;
from django.shortcuts import redirect, get_object_or_404
from customerlogin.models import Customer; 
from employee.models import service,service_provider; 
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your views here.
from django.views.decorators.cache import cache_control
from .models import payments
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from customerlogin .models import Booking,Message

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Booking
  
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    # Check if the user is logged in as admin
    if request.session.get('login') == 'admin':
        # Get the current date and time
        current_date = timezone.now()

        # Calculate the first day of the last month
        first_day_of_last_month = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)

        # Filter bookings created after the first day of the last month
        bookings_last_month = Booking.objects.filter(booking_date__gte=first_day_of_last_month)
        bookings_last_month1 = Booking.objects.filter(
            booking_date__gte=first_day_of_last_month,
            status='pending'  # Adjust this value to match the status field in your model
        )
        total_amount = bookings_last_month.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # Count the number of bookings
        booking_count = bookings_last_month.count()
        booking_count1 = bookings_last_month1.count()

        # Count the number of new customers registered last month
        total_customers = Customer.objects.count()

        # Prepare context
        context = {
            'booking_count': booking_count,
            'new_customers_last_month': total_customers,
            'first_day_of_last_month': first_day_of_last_month.strftime('%B %Y')
        }

        # Render the admin index page with the booking count and new customer count
        return render(request, 'adminindex.html', {'new_customers_last_month':total_customers,'booking_count':booking_count,'booking_count1':booking_count1,'total_amount':total_amount})
    else:
        # If not logged in as admin, redirect to login page
        return render(request, 'login1.html')
    

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def adminaccount1(request):
    if request.session.get('login') == 'admin':
       admin = request.user
       return render(request, 'accountview1.html', {'customer': admin})
    else:
        return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def editaccount2(request):
    if request.session.get('login') == 'admin':
       admin = request.user
       return render(request, 'editaccount2.html', {'customer': admin})
    else:
        return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)   
def addservice1(request):
  if request.session.get('login') == 'admin':
   
    admin = request.user
    return render(request, 'addserviceadmin.html', {'customer': admin})
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
        return redirect('admin1:displayserviceadmin')
        # Redirect to a success page
    else:
        return render(request, 'addserviceemployee.html')
    
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def edit_service(request,service_id):
  if request.session.get('login') == 'admin':
    admin = request.user
    services = get_object_or_404(service, id=service_id)
    
    return render(request, 'editservice1.html',{'data_to_display': services, 'customer': admin})


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

   
    return redirect('admin1:displayserviceadmin') 
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addserviceprovideradminview(request):
    if request.session.get('login') == 'admin':
       admin = request.user
       name=request.session.get('username')
   
       services = service.objects.all()
       data_to_display1 = []
       for services in services:
          customer_data = {
            'service_name': services.service_name,
            'id': services.id,
          }
          data_to_display1.append(customer_data)
       return render(request, 'addserviceprovideradmin.html', {'data_to_display': data_to_display1 ,'customer': admin})

    else:
        return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def changepasswordadmin(request):
    if request.session.get('login') == 'admin':
      admin = request.user
      return render(request, 'changepassword2.html', {'customer': admin})
    else:
      return render(request, 'login1.html')
    
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def editemployee(request,email):
    if request.session.get('login') == 'admin':
       employee = Employee.objects.get(email=email)
       print(employee);
    
       return render(request, 'editemployee.html', {'data_to_display': employee})
    else:
      return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def updateadminaccount(request):
   if request.session.get('login') == 'admin':  
      if request.method == 'POST':
         customer = request.user
         form = Customer(request.POST, request.FILES)
        
         first_name = request.POST['first_name']
         last_name = request.POST['last_name']
        #gender = request.POST['gender']
         phone1 = request.POST['phone']
        
        

         gender = request.POST.get('gender')
      
         file = request.FILES.get('file')
         filename = None  
         if file:
                fs = FileSystemStorage(location='customerlogin/static/images/')
                filename = fs.save(file.name, file)
                customer.photo = f'images/{filename}'


            # Update the customer record
    
         customer.first_name = first_name
         customer.last_name = last_name
         customer.gender = gender
         customer.phone1 = phone1
       
         customer.save()

         messages.success(request, 'Your profile details has been updated successfully!')
         return redirect('admin1:adminaccount1')  # Redirect to a success page
   else:

     return render(request, 'editaccount2.html', {'customer': customer})

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



def send_otp_email_employee_status(user_email,name):
 subject = 'Welcome to Expert Homecare'
 message = (
        f'Hello {name},\n\n'
        'We are excited to welcome you to the Expert Homecare team. Your account has been successfully created and you are now a part of our dedicated team.\n\n'
        'Thank you for joining us, and we look forward to a successful collaboration.\n\n'
        'Use this link to activate your account and logged into Expert Homecare account:\n'
        f'http://127.0.0.1:8000/admin1/employeepasswordadd/{user_email}/\n\n'
        'Best regards,\n'
        'Expert Homecare Team'
    )
 from_email = settings.EMAIL_HOST_USER
 recipient_list = [user_email]
 send_mail(subject, message, from_email, recipient_list)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def employeedisplay(request):
 if request.session.get('login') == 'admin':  
    customers = Employee.objects.all()  
    print(customers)
    data_to_display = []
    for customer in customers:
          customer_data = {
       
            'name': customer.name,
            'address': customer.address,
            'email': customer.email,
            'phone': customer.phone,
            'gender': customer.gender,
            'designation': customer.designation,
            'experience': customer.experience,
            'certificate_qualification': customer.certificate_qualification,
            'photo': customer.photo,
            'status': customer.status,
        }
          data_to_display.append(customer_data)
    return render(request, 'employeedisplay.html', {'data_to_display': data_to_display})
 else:
     return render(request, 'login1.html')
 
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addemployee(request):
  if request.session.get('login') == 'admin': 
    return render(request, 'adminemployee.html')
  else:
      return render(request, 'login1.html')
  
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayuser(request):
  if request.session.get('login') == 'admin': 
    customers = Customer.objects.all()  
    print(customers)
    data_to_display = []
    for customer in customers:
        if customer.status !='2':
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
  else:
     return render(request, 'login1.html')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def serviceproviderdisplay(request):
  if request.session.get('login') == 'admin':
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
    
    return render(request, 'serviceproviderdisplay.html', {'data_to_display': data_to_display})
  else:
     return render(request, 'login1.html')
  
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
 # Adjust this import based on your Customer model

def changeuserstatus(request, email):
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

    return redirect('admin1:displayuser')

from django.http import JsonResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if email already exists in the database
        if Employee.objects.filter(email=email).exists():
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


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from .models import Employee
def registeremployee(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST.get('gender')
        designation = request.POST['designation']
        experience = request.POST['experience']
        file = request.FILES['file1']
        file2 = request.FILES['file2']
        file3 = request.FILES['file3']
     
        # Save the file
        fs = FileSystemStorage(location='static/images/')
        filename = fs.save(file.name, file)
        filename2 = fs.save(file2.name, file)
        filename3 = fs.save(file3.name, file)
        send_otp_email_employee_status(email,name)
        # Create a new employee record
        employee = Employee(
            name=name,
            address=address,
            email=email,
            phone=phone,
            gender=gender,
            designation=designation,
            experience=experience,
            status="0",
            photo=f'images/{filename}',
            certificate_qualification=f'images/{filename2}',
            previous_job_work=f'images/{filename3}'
        )
        
        employee.save()
        
        messages.success(request, f'{name}\'s has been added has employee in Expert Homecare')

        return redirect('admin1:employeedisplay')  # Redirect to a view that lists employees or a success page
    else:
        return render(request, 'adminemployee.html')  # Render the form template
def disableemployee(request, email):
    try:
        customer = Employee.objects.get(email=email)
        print(customer)
        if customer.status == '3':  # Assuming 3 means active and 0 means inactive
            customer.status = "0"
            customer.save()
            messages.success(request, f'{customer.name}\'s account has been deactivated.')
        else:
            customer.status = "3"
            customer.save()
            messages.success(request, f'{customer.name} \'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('admin1:employeedisplay')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Employee

def editemployeeupdate(request, email):
    employee = get_object_or_404(Employee, email=email)
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST.get('gender')
        designation = request.POST['designation']
        experience = request.POST['experience']
        file = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')

        # Update employee fields
        employee.name = name
        employee.address = address
        employee.email = email
        employee.phone = phone
        employee.gender = gender
        employee.designation = designation
        employee.experience = experience
        employee.status="3"

        # Handle file upload
        if file:
            fs = FileSystemStorage(location='customerlogin/static/images/')
            filename = fs.save(file.name, file)
            employee.photo = f'images/{filename}'
        if file2:
            fs = FileSystemStorage(location='customerlogin/static/images/')
            filename2 = fs.save(file.name, file2)
            employee.photo = f'images/{filename2}'
        if file3:
            fs = FileSystemStorage(location='customerlogin/static/images/')
            filename3 = fs.save(file.name, file3)
            employee.photo = f'images/{filename3}'

        # Save the updated employee object
        employee.save()
        messages.success(request, 'Employee data updated successfully!')
        return redirect('admin1:employeedisplay')  # Adjust the redirect as needed
    return render(request, 'update_employee.html', {'data_to_display': employee})



@csrf_protect
def passwordaddemployee(request, email):
    if request.method == 'POST':
       employee = get_object_or_404(Employee, email=email)
       password = request.POST.get('password')
      # hashed_password = make_password(password)
       employee.status="3"
       employee.password=password
       employee.save()
       messages.success(request, 'Employee password updated Successfully.Please login with new credentials')
       return redirect('login1')
    
def employeepasswordadd(request,email):
        
    return render(request, 'employeepasswordadd.html',{'email':email})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayserviceadmin(request):
 if request.session.get('login') == 'admin': 
    services = service.objects.all()  
    print(services)
    data_to_display1 = []
    for services in services:
          customer_data = {
              'id': services.id,
            'service_name': services.service_name,
            'service_description': services.service_description,
            'photo': services.photo,
             'status': services.status,
        }
          data_to_display1.append(customer_data)

        
    return render(request, 'displayseriviceadmin.html', {'data_to_display': data_to_display1})
 else:
     return render(request, 'login1.html')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayserviceprovideradmin(request):
  if request.session.get('login') == 'admin': 
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
            'Service_Provider_gender': provider.Service_Provider_gender,
            'Service_Provider_Designation': services.service_name,
            'Service_Provider_location': provider.Service_Provider_location,
            'Service_Provider_Experience': provider.Service_Provider_Experience,
            'Service_Provider_amountdefalult': provider.Service_Provider_amountdefalult,
            'photo': provider.photo,
            'Service_Provider_Id_proof': provider.Service_Provider_Id_proof,
            'Service_Provider_Qualification_Certificate': provider.Service_Provider_Qualification_Certificate,
            'status':provider.status,
        }

        data_to_display1.append(customer_data)

    return render(request, 'displayserviceprovideradmin.html', {'data_to_display': data_to_display1})
  else:
     return render(request, 'login1.html')

def changeserviceproviderstatus2(request, service_id):
    try:
        customer = service_provider.objects.get(id=service_id)
        print(customer)
        if customer.status == '4':  # Assuming 1 means active and 0 means inactive
            customer.status = '0'
            customer.save()
            messages.success(request, f'{customer.service_provider_name}\'s account has been deactivated.')
        elif customer.status == '0' :
            customer.status = '4'
            customer.save()
            messages.success(request, f'{customer.service_provider_name} \'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('admin1:displayserviceprovideradmin')



def enable_disable_service(request, service_id):
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
    return redirect('admin1:displayserviceadmin') 

def updateadminpassword(request):
    if request.method == 'POST':
        customer = request.user
        form = Customer(request.POST, request.FILES)
        
        password = request.POST['password']
        hashed_password = make_password(password)
        customer.password = hashed_password
       
        customer.save()

        messages.success(request, 'Your profile password has been updated successfully! Please login again')
        return redirect('login1')  # Redirect to a success page
   

    return render(request, 'changepassword2.html', {'customer': customer})
from django.core.cache import cache


def logoutadmin(request):
    cache.clear()
    request.session['login'] = " "
    request.session['id'] = " "
    
    # Redirect to a success page or login page
    return redirect('login1')

def payment(request,booking_id):
      request.session['bookingid'] =booking_id
      customer = Booking.objects.get(id=booking_id)
      paymentamount=(customer.amount)
      paymentamount=int(paymentamount)*100
      print(paymentamount)
      return render(request, 'payment.html', {'paymentamount': paymentamount})
      
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import payments, Booking
from datetime import datetime

@csrf_exempt
def updatepayment(request):
    if request.method == 'POST':
        print("Hello")
        
        # Get the booking ID from the session
        bookingid = request.session.get('bookingid') 
        if not bookingid:
            return JsonResponse({'error': 'Booking ID not found in session.'}, status=400)

        try:
            # Retrieve the Booking instance
            booking = Booking.objects.get(id=bookingid)
            
            # Update the payment status for the booking
            booking.paymentstatus = "Done"
            booking.save()

            # Get the payment ID from the POST request
            payid = request.POST.get('pay_id')
            today_date = datetime.now().strftime("%Y-%m-%d")
            # Create a new payment entry
            payment = payments.objects.create(
                Payment_id=payid,
                booking_id=booking,  # Pass the Booking instance, not just the ID
                transactiondate=today_date,
                status="Done"

                
            )

            # Save the payment entry
            payment.save()

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Payment recorded successfully'})
        
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Invalid booking ID.'}, status=400)
        
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

   
def addserviceproviderdata(request):
    if request.method == 'POST':
        name=request.session.get('username')
     
      
        service_provider_name = request.POST['name']
        Service_Provider_Address = request.POST['address']
        Service_Provider_Email = request.POST['email']
        Service_Provider_Phone = request.POST['phone']
        Service_Provider_gender = request.POST['gender']
        Service_Provider_location = request.POST['location']
        Service_Provider_basicamount = request.POST['amount']
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
            Service_Provider_location=Service_Provider_location,
            Service_Provider_basicamount=Service_Provider_basicamount,
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
        return redirect('admin1:displayserviceprovideradmin')
        # Redirect to a success page
    else:
        return render(request, 'addserviceprovideradmin.html')

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

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayserviceproviderdataeditpage(request,id1):
  if request.session.get('login') == 'admin': 
    customer = request.user
    data_to_display1 = []
    data_to_display = []
    
 
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
 
   
    customer_data = {
            'id': serviceprovider_id.id,
            'service_name': serviceprovider_id.service_provider_name,
            'service_address': serviceprovider_id.Service_Provider_Address,
            'Service_Provider_Email': serviceprovider_id.Service_Provider_Email,
            'Service_Provider_Phone': serviceprovider_id.Service_Provider_Phone,
            'Service_Provider_gender': serviceprovider_id.Service_Provider_gender,
            'Service_Provider_Designation': servicename1.service_name,
             'Service_Provider_service_id': serviceprovider_id.service_table,
            'Service_Provider_location': serviceprovider_id.Service_Provider_location,
            'Service_Provider_Experience': serviceprovider_id.Service_Provider_Experience,
            'Service_Provider_amountdefalult':serviceprovider_id.Service_Provider_amountdefalult,
            'photo': serviceprovider_id.photo,
            'Service_Provider_Id_proof': serviceprovider_id.Service_Provider_Id_proof,
            'Service_Provider_Qualification_Certificate': serviceprovider_id.Service_Provider_Qualification_Certificate,
            'status':serviceprovider_id.status,
        }

    data_to_display1.append(customer_data)

    return render(request, 'serviceprovideredit1.html', {'service_provider': data_to_display1,'service': data_to_display,'customer':customer})
  else:
     return render(request, 'login1.html')

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
        Service_Provider_location = request.POST['location']
        Service_Provider_basicamount = request.POST['amount']
        Service_Provider_Experience = request.POST['experience']
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
        employee.Service_Provider_amountdefalult=Service_Provider_basicamount
        employee.Service_Provider_location=Service_Provider_location
        employee.service_table=Service_Provider_Designation
        employee.Service_Provider_Experience=Service_Provider_Experience
        # Create a new customer record
        
        employee.save()
        messages.success(request, 'Service Provider Details Updated Sucessfully!')
        return redirect('admin1:displayserviceprovideradmin')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)    
def viewbookingadmin(request):
    if request.session.get('login') == 'admin':
        employee=request.user;
        bookings = Booking.objects.all()
        
        filtered_bookings = []
        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)
            
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
        
        return render(request, 'viewbookingadmin.html', {'data_to_display': filtered_bookings,'customer':employee})
    else:
        return render(request, 'login1.html')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def transactionadmin(request):
  if request.session.get('login') == 'admin':
    employee=request.user;
    # Fetch all payments
    payments_list = payments.objects.all().order_by('-transactiondate')

    transaction_details = []

    for payment in payments_list:
        booking = payment.booking_id
        service_provider = booking.service_provider
        service1 = get_object_or_404(service, id=service_provider.service_table)

        transaction_detail = {
            'Transaction_Id': payment.Payment_id,
            'booking_id': booking.id,
            'service_name': service1.service_name,
            'service_provider_name': service_provider.service_provider_name,
            'service_provider_email': service_provider.Service_Provider_Email,
            'service_provider_phone': service_provider.Service_Provider_Phone,
            'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
            'customer_email': booking.customer.email,
            'customer_phone': booking.customer.phone1,
            'transactiondate': payment.transactiondate,
            'amount': booking.amount,
            'payment_status': payment.status,
        }

        transaction_details.append(transaction_detail)

    context = {
        'transaction_details': transaction_details,
    }

    return render(request, 'transaction.html', { 'transaction_details': transaction_details,'customer':employee})

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Booking

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
from django.shortcuts import render
from .models import Booking

def booking_report_pdf(request):
    # Fetch all bookings ordered by booking_date in descending order
    bookings = Booking.objects.all().order_by('-booking_date')

    # Format booking dates to exclude time
    formatted_bookings = [
        {
            'id': booking.id,
            'service_provider_name': booking.service_provider.service_provider_name,
            'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
            'address': booking.address,
            'booking_date': booking.booking_date.date(),  # Show only the date
            'amount': booking.amount,
            'status': booking.status,
        }
        for booking in bookings
    ]

    context = {
        'bookings': formatted_bookings,
    }

    return render(request, 'bookingreport.html', context)



from django.shortcuts import render
from .models import Employee
from datetime import datetime

def employeeppdf(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
        'current_year': datetime.now().year  # Add this if you're using current_year in your template
    }
    return render(request, 'employeepdf.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.utils import timezone
from django.conf import settings
 # Make sure to import the service model

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None




def servicepdf(request):
  
        # Fetch all service providers
        service_providers = service.objects.all()

        providers_data = []
        for provider in service_providers:
        
            provider_data = {
                'service_name': provider.service_name,
                'service_description': provider.service_description,
                'photo': provider.photo,
               
            }
            providers_data.append(provider_data)

        # Prepare the context
        context = {
            'services': providers_data,
            'current_year': timezone.now().year
        }

        return render(request, 'servicepdf.html', context)
  
@cache_control(no_cache=True, no_store=True, must_revalidate=True)   
def serviceproviderpdf(request):
    if request.session.get('login') == 'admin':
        # Fetch all service providers
        service_providers = service_provider.objects.all()

        providers_data = []
        for provider in service_providers:
            service_obj = get_object_or_404(service, id=provider.service_table)
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
    

def customerpdf(request):
   
        # Fetch all service providers
        service_providers = Customer.objects.all()

        providers_data = []
        for provider in service_providers:
      
            provider_data = {
                'first_name': provider.first_name,
                'last_name': provider.last_name,
                'gender': provider.gender,
                'address': provider.address,
                'email': provider.email,
                'phone1': provider.phone1,
              
                
                'photo': provider.photo,
            
            }
            providers_data.append(provider_data)

        # Prepare the context
        context = {
            'customers': providers_data,
            'current_year': timezone.now().year
        }

        return render(request, 'customerpdf.html', context)
  

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def transactionpdf(request):
    if request.session.get('login') == 'admin':
        # Fetch all payments
        payments_list = payments.objects.all().order_by('-transactiondate')

        transaction_details = []

        for payment in payments_list:
            booking = payment.booking_id
            service_provider = booking.service_provider
            service_obj = get_object_or_404(service, id=service_provider.service_table)

            transaction_detail = {
                'Transaction_Id': payment.Payment_id,
                'booking_id': booking.id,
                'service_name': service_obj.service_name,
                'service_provider_name': service_provider.service_provider_name,
                'service_provider_email': service_provider.Service_Provider_Email,
                'service_provider_phone': service_provider.Service_Provider_Phone,
                'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                'customer_email': booking.customer.email,
                'customer_phone': booking.customer.phone1,
                'transactiondate': payment.transactiondate,
                'amount': booking.amount,
                'payment_status': payment.status,
            }

            transaction_details.append(transaction_detail)

        # Prepare the context
        context = {
            'transaction_details': transaction_details,
            'current_year': timezone.now().year,
        }

        return render(request, 'transcationpdf.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')


from django.db.models import OuterRef, Subquery
 # Import your Message and Customer models

from django.db.models import OuterRef, Subquery
from django.shortcuts import render
 # Import your models

def admin_chat_view(request):
    admin_email = 'mathew@gmail.com'  # Admin email (replace if needed)

    # Get all users for the admin to select from (excluding the admin)
    users = Customer.objects.exclude(email=admin_email)

    # Subquery to fetch the last message for each user
    last_message_subquery = Message.objects.filter(
        recipient=OuterRef('pk')  # Assuming 'recipient' refers to the user (Customer)
    ).order_by('-timestamp').values('content')[:1]  # Get the latest message's content

    # Annotate users with their last message
    users = users.annotate(last_message=Subquery(last_message_subquery))

    # Get all messages sent to the admin (ordered by timestamp)
    messages = Message.objects.filter(recipient__email=admin_email).order_by('timestamp')

    context = {
        'messages': messages,  # Messages received by admin
        'users': users,        # Users list with their last message
        'admin_email': admin_email,  # Admin email for reference
    }

    return render(request, 'users.html', context)


from django.http import JsonResponse
# Assuming your model is named Customer

def search_users(request):
    if request.method == 'POST':
        search_term = request.POST.get('searchTerm', '')
        users = Customer.objects.filter(name__icontains=search_term)  # Adjust field as necessary
        user_list = [{'name': user.name, 'email': user.email} for user in users]  # Adjust based on your model
        return JsonResponse(user_list, safe=False)

def get_users(request):
    users = Customer.objects.all()  # Get all users
    user_list = [{'name': user.name, 'email': user.email} for user in users]  # Adjust based on your model
    return JsonResponse(user_list, safe=False)


from django.shortcuts import render, get_object_or_404


def chat_with_customer_view(request, user_email):
    customer = get_object_or_404(Customer, email=user_email)
    print(customer.photo)
    request.session["user_email"]=user_email;
    request.session["photo"] = customer.photo.url if customer.photo else None
    
    # Retrieve messages between the admin and this customer
    messages = Message.objects.filter(sender__email=user_email, recipient__email='mathew@gmail.com') | \
               Message.objects.filter(sender__email='mathew@gmail.com', recipient__email=user_email)
    messages = messages.order_by('timestamp')

    context = {
        'customer': customer,
        'messages': messages,
    }
    return render(request, 'chatadmin.html', context)


from django.shortcuts import render, redirect


from django.shortcuts import render, get_object_or_404



def chatadmin(request, user_email=None):
    # Ensure user_email is set from session during POST requests
    if request.method == 'POST':
        user_email = request.session.get('user_email')
  
        if not user_email:
            # If no user email in session, return some error or redirect
            return redirect('some_error_page')  # Redirect or handle error appropriately

        customer = get_object_or_404(Customer, email=user_email)
        message_content = request.POST.get('message')

        if message_content:
            try:
                # Admin email is fixed here as 'mathew@gmail.com'
                sender = get_object_or_404(Customer, email='mathew@gmail.com')  # Admin user
                
                # Create and save a new message from the admin to the customer
                message = Message.objects.create(sender=sender, recipient=customer, content=message_content)
                print(f"Message sent by admin: {message_content}")
            except Customer.DoesNotExist:
                print("Customer or Admin not found")

    # Fetch the customer and admin messages, even during GET request
    if user_email:
        admin = get_object_or_404(Customer, email='mathew@gmail.com')  # Admin user
        customer = get_object_or_404(Customer, email=user_email)

        # Fetch both sent and received messages between the admin and the customer
        messages = Message.objects.filter(sender=admin, recipient=customer).union(
            Message.objects.filter(sender=customer, recipient=admin)
        ).order_by('timestamp')

        # Print all fetched messages for debugging purposes
        for message in messages:
            print(f"Message Content: {message.content}")

        context = {
            'messages': messages,  # Pass the list of messages
            'customer': customer,  # Pass the customer object
        }
    else:
        context = {
            'messages': [],  # No messages if no user email
            'customer': None,
        }

    return render(request, 'chatadmin.html', context)

from customserviceprovider.models import Feedback 

def display_feedback1(request):

    if request.session.get('login') == 'admin':
     
        employee=request.user;

        # Fetch feedback data from the database, filtering by the logged-in service provider
        feedbacks = Feedback.objects.all() # Adjust the query as needed

        # Pass the data to the template
        context = {
            'data_to_display': feedbacks,
            'messages': request.session.pop('messages', []), 
            'customer': employee,  # Handle messages if any
        }
        print(context)
        return render(request, 'displayfeedbackadmin.html', context)
    else:
        return render(request, 'login1.html')  # Redirect to login page








