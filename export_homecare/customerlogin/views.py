from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from .models import Customer,Booking
from custadmin.models import Employee,payments;
from employee.models import service,service_provider;   # Import your Customer model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
from customserviceprovider.models import Accessoriesbuy
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.
# def registercustomer(request):
#     if request.method=="POST":
#        first=request.POST['first_name']
#        last=request.POST['last_name']
#        gender=request.POST['gender']
#        phone1=request.POST['phone1']
#        email=request.POST['email']
#        file=request.POST['file']
#        pass1=request.POST['pass']
#        cpass=request.POST['cpass']
#        myuser=User.objects.create_user(username=email,password=pass1,first_name=first,last_name=last)
#        myuser.save()
#        return redirect('home')
#     return render(request,'register.html')

def forgot(request):
    return render(request,'forgot.html')

def service1(request):
    services = service.objects.filter(status=1)
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

    return render(request,'service.html', {'data_to_display': data_to_display1})
def servicelogin(request):
   if request.session.get('login') == 'yes':
    services = service.objects.filter(status=1) 
    customer = request.user
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

    return render(request,'servicelogin.html', {'data_to_display': data_to_display1,'customer': customer})
   else:
     return render(request, 'login1.html')


def register(request):
    return render(request,'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login1(request):
    return render(request, 'login1.html')

def home(request):
   
      return render(request, 'index.html')
   

def emailverify(request):
    return render(request, 'emailverify.html')

@login_required
def userloginhome(request):
    request.session['login'] = 'yes'
    customer = request.user  # Get the logged-in user
 
    return render(request, 'userloginhome.html', {'customer': customer})
    

def useraccount(request):
    customer = request.user 
     # Get the logged-in user
    if request.session.get('login') == 'yes':
       return render(request, 'accountview.html', {'customer': customer})
    else:
        return render(request, 'login1.html')
    
def editaccount(request):
    customer = request.user  # Get the logged-in user
    if request.session.get('login') == 'yes':
       return render(request, 'editaccount.html', {'customer': customer})
    else:
        return render(request, 'login1.html')
def updatepassword(request):
    
    customer = request.user  # Get the logged-in user
    if request.session.get('login') == 'yes':
        return render(request, 'changepassword.html', {'customer': customer})
    else:
        return render(request, 'login1.html')
def deactiveaccountuser(request):
    customer = request.user  # Get the logged-in user
    if request.session.get('login') == 'yes':
       return render(request, 'deactiveuseraccount.html', {'customer': customer})
    else:
        return render(request, 'login1.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

def send_otp_email(user_email, otp):
    subject = 'OTP for Password Reset'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

def send_otp_emailregister(user_email, otp):
    subject = 'OTP for Email Registration on Expert Homecare Account'
    message = (
    f"Hello,\n\n"
    f"Thank you for registering with Expert Homecare!\n\n"
    f"To complete your registration, please use the following One-Time Password (OTP):\n\n"
    f"{otp}\n\n"
    f"This OTP is valid for a short period of time. If you did not request this registration, please ignore this email.\n\n"
    f"Best regards,\n"
    f"The Expert Homecare Team"
    )
 
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['username']
        try:
            user = Customer.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='1234567890')
            request.session['otp'] = otp # Store OTP in session for verification
            request.session['email'] = email  
            send_otp_email(user.email, otp)
            messages.success(request, 'OTP Send Successfully')
            return render(request, 'verify_otp.html')
        except Customer.DoesNotExist:
            messages.error(request, 'User Not Found')
            return render(request, 'forgot.html')
    return render(request, 'forgot.html')

def registeremail(request,email):
            user = Customer.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='1234567890')
            request.session['otp'] = otp # Store OTP in session for verification
            request.session['email'] = email
            send_otp_emailregister(user.email, otp)
            
 
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session.get('otp'):
            return render(request, 'change_password.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html', {'error': 'Invalid OTP. Please try again.'})
   
def verify_otp1emailset(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session.get('otp'):
            email=request.session.get('email')
            customer = Customer.objects.get(email=email)
            print(customer)
            customer.status='1'
            customer.save()
            messages.success(request, 'Account Registered Successfully.')
            return render(request, 'login1.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'emailverify.html')
    return render(request, 'emailverify.html', {'error': 'Invalid OTP. Please try again.'})
   

from django.contrib.auth.hashers import make_password

def change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['cpassword']
        if password == confirm_password:
            # Reset the user's password
            user = Customer.objects.get(email=request.session.get('email'))
            user.set_password(password)
            user.save()
            messages.success(request, 'Password changed successfully. Please login with your new password.')
            return redirect('login1')  # Redirect to login page
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
    return render(request, 'change_password.html')


def registercustomer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST.get('gender')
        phone1 = request.POST['phone1']
        email = request.POST['email']
        passw = request.POST['pass']
        cpass = request.POST['cpass']
        # file = request.FILES.get('file', None)

        if passw != cpass:
            return HttpResponse("Passwords do not match")

        # Save the file
        hashed_password = make_password(passw)
       
        # fs = FileSystemStorage(location=f'customerlogin/static/images/')
        # filename = fs.save(file.name, file)
        # Create a new customer record
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone1=phone1,
            email=email,
            password=hashed_password,  # You might want to hash this before saving
            # photo=f'images/{filename}'
        )
        customer.save()
        registeremail(request,email) 
      
        return render(request, 'emailverify.html')
        # Redirect to a success page
    else:
        return render(request, 'forgotpassword1emailset')
    

  




def changepassworduser(request):
    if request.method == 'POST':
        customer = request.user
        form = Customer(request.POST, request.FILES)
        
        password = request.POST['password']
       

            # Update the customer record
        hashed_password = make_password(password)
        customer.password = hashed_password
        
       
       
        customer.save()

        messages.success(request, 'Your account password has been updated successfully!')
        update_session_auth_hash(request, customer)
        customer = request.user  # Get the logged-in user
        return render(request, 'accountview.html', {'customer': customer}) # Redirect to a success page
   

    return render(request, 'changepassword.html')
def updatecustomerdata(request):
    if request.method == 'POST':
        customer = request.user
        form = Customer(request.POST, request.FILES)
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        #gender = request.POST['gender']
        phone1 = request.POST['phone1']
        filenotupdate = request.POST['file1']
        
        address = request.POST.get('address')
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
        customer.address=address
        customer.phone1 = phone1
       
        customer.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('useraccount')  # Redirect to a success page
   

    return render(request, 'editaccount.html', {'customer': customer})
def updatecustomerdata1(request):
    if request.method == 'POST':
        customer = request.user
        form = Customer(request.POST, request.FILES)
        
        
      
        file = request.FILES.get('file')
        filename = None  
        if file:
                fs = FileSystemStorage(location='customerlogin/static/images/')
                filename = fs.save(file.name, file)
                customer.photo = f'images/{filename}'


            # Update the customer record
    
      
        customer.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('useraccount')  # Redirect to a success page
   

    return render(request, 'editaccount.html', {'customer': customer})

def deactivefunctionuser(request):
  if request.method == 'POST':
        customer = request.user
        request.user.status = '0'
        request.user.save()
        messages.success(request, 'Your account has been deactivated.')
        return redirect('login1')  # Redirect to a safe place, e.g., home page
  else:
    return render(request, 'useraccount')


from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login


def logincustomer(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
      
     #   Authenticate user with email, password, and status check ('1' for customers)
        user = authenticate(request, email=email, password=password)
        # print(user);
      
    
        
        if user is not None:
            # Check if the authenticated user is a customer
            try:
                customer = Customer.objects.get(email=user.email)
                login(request, user)
                if(customer.status=='1'):
                    request.session['login'] = 'yes'
                    return redirect("userloginhome") 
                elif(customer.status=='2'):
                    request.session['login'] = 'admin'
                    return redirect('admin1:index') 
                    
                else:
                     messages.success(request, 'Your account is in deactivated mode.')
                     return render(request, 'login1.html')

                
                
            
            except Customer.DoesNotExist:
                # Handle case where Customer record doesn't exist
                return HttpResponse("Customer record not found.")
 
        elif email and password :
          try:
           employee = Employee.objects.get(email=email)
     
           
           if employee.email==email and employee.password==password and employee.status=="3":
         
            # Authenticate user with email and password only (without status check)
            # login(request, user)
            name=employee.name;
            id=employee.id;
            request.session['username']=name;
            request.session['id']=id;
            request.session['login'] = 'employee'
            name=request.session.get('username')
            return redirect('employee:index1') 
           else:
               messages.success(request, 'Account is not activated.')
               return render(request, 'login1.html')
           
          except Employee.DoesNotExist:
              try:
               serviceprovider = service_provider.objects.get(Service_Provider_Email=email)
               if serviceprovider.Service_Provider_Email==email and serviceprovider.password==password and serviceprovider.status=="4":
                print(serviceprovider.Service_Provider_Email)
                print(serviceprovider.password);
                print(serviceprovider.status);
            # Authenticate user with email and password only (without status check)
            # login(request, user)
                name=serviceprovider.service_provider_name;
                id=serviceprovider.id;
                request.session['username']=name;
                request.session['id']=id;
                request.session['login'] = 'serviceprovider'
                name=request.session.get('username')
                return redirect('customserviceprovider:index2') 
              except service_provider.DoesNotExist:
                    messages.error(request, 'Invalid credentials.')
                    return render(request, 'login1.html')
            
            
            
        else:
                # Authentication failed
            messages.success(request, 'Invalid credentials')
            return render(request, 'login1.html', {'error': 'Invalid credentials'})
    
    messages.success(request, 'Invalid credentials')
    return render(request, 'login1.html', {'error': 'Invalid credentials'})


from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def handle_google_login(request):
    try:
        # Attempt to retrieve the Google account associated with the authenticated user
        google_account = SocialAccount.objects.get(provider='google', user=request.user)
       
        # Google account already associated, redirect to profile page
        return redirect('profile')
    
    except SocialAccount.DoesNotExist:
        # If Google account is not already associated, proceed with normal Google login flow
        # This part typically handles the OAuth flow for Google login
        # Ensure this matches your existing Google OAuth configuration
        return redirect('social:begin', 'google-oauth2')

    except Exception as e:
        # Handle any other exceptions or errors that may occur during the process
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')  # Redirect to an appropriate page

    # Additional handling or fallback logic can be added here as needed


from django.shortcuts import render

# views.py  
from django.shortcuts import render

def custom_error_view(request):
    return render(request, 'custom_error_template.html', {
        'message': 'This Google account is already in use. Please use a different account or contact support for assistance.'
    })
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page or login page
    return redirect('login1')



# customerlogin/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer  # Import your Customer model here

@csrf_exempt
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if email already exists in the database
        if Customer.objects.filter(email=email).exists():
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


def viewserviceprovider(request, id):
  if request.session.get('login') == 'yes':
    try:
        service_providers = service_provider.objects.all(status=4)  
        print(service_providers)
        data_to_display = []
      #  print(id)
        
        for provider in service_providers:
            if provider.service_table == id:
                customer_data = {
                    'service_provider_id': provider.id,
                    'service_provider_name': provider.service_provider_name,
                    'Service_Provider_Experience': provider.Service_Provider_Experience,
                    'Service_Provider_Phone': provider.Service_Provider_Phone,
                    'Service_Provider_Email': provider.Service_Provider_Email,
                    'Service_Provider_gender': provider.Service_Provider_gender,
                    'Service_Provider_location': provider.Service_Provider_location,
                    'Service_Provider_amountdefalult': provider.Service_Provider_amountdefalult,
                    'photo': provider.photo,
                }
                data_to_display.append(customer_data)

        if not data_to_display:
            customer_data = {
                'error': 'No service providers found for the given ID.'
            }
            data_to_display.append(customer_data)

        return render(request, 'viewserviceprovider.html', {'data_to_display': data_to_display})

    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'viewserviceprovider.html', {'error': 'An error occurred while fetching data.'})
  else:
                # Authentication failed
       
      return render(request, 'login1.html')


from employee.models import service,service_provider;  
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
 # Ensure these are the correct model names

def fetch_providers_by_filters(request, id):
    # Retrieve filter parameters from the request
    location = request.GET.get('location')
    experience = request.GET.get('experience')
    print(experience)

   
    

    # Apply filters based on parameters
    providers = service_provider.objects.filter(service_table=id , status=4)  # Start with all providers for the given service_table

    if location:
        providers = providers.filter(Service_Provider_location=location)
    
    if experience:
        try:
            experience = int(experience)
            if experience == 1:
                experience_min, experience_max = 1, 4
            elif experience == 5:
                experience_min, experience_max = 5, 8
            elif experience == 9:
                experience_min, experience_max = 9, 30
            providers = providers.filter(
                Service_Provider_Experience__gte=experience_min,
                Service_Provider_Experience__lte=experience_max
            )
        except ValueError:
            pass  # Handle the case where conversion fails

    data = {
        'providers': []
    }

    for provider in providers:
        try:
            service1 = service.objects.get(id=provider.service_table)
            service_name = service1.service_name
            print(service1.service_name)
        except service.DoesNotExist:
            service_name = "Unknown"  # Default value if service not found

        data['providers'].append({
            'service_provider_name': provider.service_provider_name,
            'Service_Provider_Email': provider.Service_Provider_Email,
            'Service_Provider_Phone': provider.Service_Provider_Phone,
            'Service_Provider_gender': provider.Service_Provider_gender,
            'Service_Provider_Experience': provider.Service_Provider_Experience,
            'photo': provider.photo.url,
            'Service_Provider_location': provider.Service_Provider_location,
             'Service_Provider_amountdefalult': provider.Service_Provider_amountdefalult,
            'service_name': service_name,  # Add the service name to the response
            'id': provider.id,
        })
  
    return JsonResponse(data)



from django.shortcuts import render
from django.http import JsonResponse
from .models import Booking, service_provider
from datetime import timedelta


from django.shortcuts import render, get_object_or_404
from .models import Booking, service_provider, BookingDate
from datetime import timedelta
import json

def bookingservice(request):
   if request.session.get('login') == 'yes':
    provider_id = request.GET.get('provider_id')
    print(provider_id)
    serviceprovider = get_object_or_404(service_provider, id=provider_id)
    print(serviceprovider.id)
    data_to_display = []
    
    customer_data = {
        'service_provider_id': serviceprovider.id,
        'service_provider_name': serviceprovider.service_provider_name,
        'Service_Provider_Experience': serviceprovider.Service_Provider_Experience,
        'Service_Provider_Phone': serviceprovider.Service_Provider_Phone,
        'Service_Provider_Email': serviceprovider.Service_Provider_Email,
        'Service_Provider_gender': serviceprovider.Service_Provider_gender,
        'Service_Provider_location': serviceprovider.Service_Provider_location,
        'photo': serviceprovider.photo,
    }
    data_to_display.append(customer_data)
   

    # Fetch booked dates and time slots
    bookings = Booking.objects.filter(service_provider=serviceprovider)
    booked_slots = {}

    for booking in bookings:
        booked_dates = BookingDate.objects.filter(booking=booking)
        for booked_date in booked_dates:
            date_str = booked_date.service_start_date.strftime('%Y-%m-%d')
            if date_str not in booked_slots:
                booked_slots[date_str] = []
            booked_slots[date_str].append(booked_date.time_slot)
            print(data_to_display)
    return render(request, 'multipledate.html', {
        'service_provider_name': data_to_display,
        'booked_slots': json.dumps(booked_slots)  # Pass booked slots as JSON
    })
   else:
       
      return render(request, 'login1.html', {'error': 'Invalid credentials'})




from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Booking, BookingDate

def book_service(request):
    if request.method == 'POST':
        
        provider_id = request.POST.get('serviceid')
       

        service_provider1 = get_object_or_404(service_provider, id=provider_id)
        address = request.POST.get('address')
        start = request.POST.get('dates')  # Expecting a comma-separated string of dates
        time_slots = request.POST.get('timeslot') 
        print(time_slots) # Expecting a comma-separated string of time slots
        detail = request.POST.get('detail')
        customer_id = request.POST.get('customer_id')
        customer = get_object_or_404(Customer, id=customer_id)
        
        # Convert date string to the proper format
        try:
            old_format = '%d-%m-%Y'
            new_format = '%Y-%m-%d'
            
            # If `start` contains multiple dates, split them and convert
            start_dates = start.split(',')
            time_slots = time_slots.split(',')
           
            
            # Ensure both lists have the same length
            if len(start_dates) != len(time_slots):
                return render(request, 'multipledate.html', {'error': 'Mismatch between dates and time slots.'})
            
            formatted_start_dates = [datetime.strptime(date.strip(), old_format).strftime(new_format) for date in start_dates]

            today_date = datetime.today().date()

        except ValueError:
            return render(request, 'multipledate.html', {'error': 'Invalid date format. Use DD-MM-YYYY.'})

        # Save the booking
        booking = Booking(
            service_provider=service_provider1,
            customer=customer,
            address=address,
            amount="pending",
            booking_date=today_date,
            notes=detail,
            status="pending",
            paymentstatus="pending",
        )
        booking.save()

        # Save each booking date with time slot
        for start_date, time_slot in zip(formatted_start_dates, time_slots):
            BookingDate.objects.create(
                booking=booking,
                service_start_date=start_date,
                time_slot=time_slot.strip()
            )
        
        # Redirect to a success page or render a success template
        return redirect('bookview')
       
    
    else:
        return render(request, 'multipledate.html')
    
    





from django.utils.dateparse import parse_date
from django.http import JsonResponse
from .models import Booking
from datetime import datetime

def check_date_availability(request):
    if request.method == "POST":
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        # Convert dates from string to datetime objects
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()
        
        # Check if start date is greater than end date
        if start_date > end_date:
            return JsonResponse({'available': None, 'error': 'Invalid date range: Start date is greater than end date.'})
        
        # Check if the date range overlaps with any existing bookings
        overlapping_bookings = Booking.objects.filter(
            service_start_date__lte=end_date,
            service_end_date__gte=start_date
        )
        
        available = not overlapping_bookings.exists()
        
        return JsonResponse({'available': available})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# def bookview(request):
#     services = Booking.objects.all()  
#     customer = request.user
#     print(services)
#     data_to_display1 = []
#     for services in services:
#           customer_data = {
#               'id': services.id,
#             'service_name': services.service_name,
#             'service_description': services.service_description,
#             'photo': services.photo,
#         }
#           data_to_display1.append(customer_data)

#     return render(request,'mybooking.html', {'data_to_display': data_to_display1,'customer': customer})

# from django.shortcuts import render, get_object_or_404
# from django.utils.dateformat import format as date_format
# from .models import Booking, BookingDate, service

# def bookview(request):
#   if request.session.get('login') == 'yes':
#     customer = request.user
#     print(customer.id)
#     # Fetch all bookings with related customer, service provider, and service details
#     bookings = Booking.objects.filter(customer_id=customer.id).select_related('customer', 'service_provider').order_by('-id')
   
    
#     data_to_display = {}

#     for booking in bookings:
#         # Fetch the related service provider instance
#         provider = booking.service_provider
#         # Fetch the related service instance
#         service1 = provider.service_table
#         service2 = get_object_or_404(service, id=service1)  # Ensure you have the correct service relation
        
#         # Fetch related BookingDate instances
#         booking_dates = BookingDate.objects.filter(booking=booking)
        
#         # Group booking dates and time slots
#         date_slots = []
#         for booking_date in booking_dates:
#             date_slots.append({
#                 'service_start_date': date_format(booking_date.service_start_date, 'd M Y'),  # Format the date
#                 'time_slot': booking_date.time_slot,
#             })

#         # Prepare booking details
#         booking_data = {
#             'booking_id': booking.id,
#             'address': booking.address,
#             'notes': booking.notes,
#             'amount': booking.amount,
#             'status': booking.status,
#             'date_slots': date_slots,
#             'paymentstatus':booking.paymentstatus,
#             'service_provider_name': provider.service_provider_name,
#             'service_provider_email': provider.Service_Provider_Email,
#             'service_provider_phone': provider.Service_Provider_Phone,
#             'service_provider_location': provider.Service_Provider_location,
#             'service_name': service2.service_name,
#             'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
#             'customer_email': booking.customer.email,
#             'customer_phone': booking.customer.phone1,
#         }

#         data_to_display[booking.id] = booking_data
#         print(data_to_display)

#     return render(request, 'mybooking.html', {'data_to_display': data_to_display, 'customer':customer})
  
#   else:
#       return render(request, 'login1.html')


from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import format as date_format
from .models import Booking, BookingDate, service  # Import the Payment model

def bookview(request):
    if request.session.get('login') == 'yes':
        customer = request.user
      
        
        # Fetch all bookings with related customer, service provider, and service details
        bookings = Booking.objects.filter(customer_id=customer.id).select_related('customer', 'service_provider').order_by('-id')
        
        data_to_display = {}

        for booking in bookings:
            # Fetch the related service provider instance
            provider = booking.service_provider
            # Fetch the related service instance
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)  # Ensure you have the correct service relation
            
            # Fetch related BookingDate instances
            booking_dates = BookingDate.objects.filter(booking=booking)
            
            # Fetch payment details related to this booking
            payment = payments.objects.filter(booking_id=booking.id).first()  # Assuming one payment per booking
            
            # Fetch Accessoriesbuy details related to this booking
            accessoriesbuy = Accessoriesbuy.objects.filter(Booking1=booking).first()  # Assuming one Accessoriesbuy per booking
            
            # Group booking dates and time slots
            date_slots = []
            for booking_date in booking_dates:
                date_slots.append({
                    'service_start_date': date_format(booking_date.service_start_date, 'd M Y'),  # Format the date
                    'time_slot': booking_date.time_slot,
                })

            # Prepare booking details
            booking_data = {
                'booking_id': booking.id,
                'address': booking.address,
                'notes': booking.notes,
                'amount': booking.amount,
                'status': booking.status,
                'date_slots': date_slots,
                'paymentstatus': booking.paymentstatus,
                'service_provider_name': provider.service_provider_name,
                'service_provider_email': provider.Service_Provider_Email,
                'service_provider_phone': provider.Service_Provider_Phone,
                'service_provider_location': provider.Service_Provider_location,
                'service_name': service2.service_name,
                'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                'customer_email': booking.customer.email,
                'customer_phone': booking.customer.phone1,
            }

            # Add payment details if available
            if payment:
                booking_data['payment_id'] = payment.Payment_id
                booking_data['payment_status'] = payment.status

            # Add Accessoriesbuy details if available
            if accessoriesbuy:
                booking_data['accessoriesbuy_amount'] = accessoriesbuy.Additionalaccessoriesamount
                booking_data['accessoriesbuy_proof'] = accessoriesbuy.proofupdate.url  # Provide URL to the image
                booking_data['accessoriesbuy_update_date'] = date_format(accessoriesbuy.update_date, 'd M Y')  # Format the date

            data_to_display[booking.id] = booking_data
           

        return render(request, 'mybooking.html', {'data_to_display': data_to_display, 'customer': customer})
    
    else:
        return render(request, 'login1.html')
      
from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import format as date_format
from .models import Booking, BookingDate, service

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

def editbooking(request, id):
    booking = get_object_or_404(Booking, id=id)
   
    if request.session.get('login') == 'yes':
        customer = request.user
        
        bookings = Booking.objects.filter(id=booking.id).select_related('customer', 'service_provider')
        
        data_to_display = {}
        booked_slots = {}

        for booking in bookings:
            provider = booking.service_provider
            service2 = get_object_or_404(service, id=provider.service_table)
            
            booking_dates = BookingDate.objects.filter(booking=booking)
            
            date_slots = []
            for booking_date in booking_dates:
                date_str = booking_date.service_start_date.strftime('%Y-%m-%d')
                time_slot = booking_date.time_slot
                if date_str not in booked_slots:
                    booked_slots[date_str] = []
                booked_slots[date_str].append(time_slot)

                date_slots.append({
                    'service_start_date': booking_date.service_start_date,
                    'time_slot': time_slot,
                })

            booking_data = {
                'booking_id': booking.id,
                'address': booking.address,
                'notes': booking.notes,
                'status': booking.status,
                'date_slots': date_slots,
                'service_provider_name': provider.service_provider_name,
                'service_provider_email': provider.Service_Provider_Email,
                'service_provider_phone': provider.Service_Provider_Phone,
                'service_provider_location': provider.Service_Provider_location,
                'service_name': service2.service_name,
                'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                'customer_email': booking.customer.email,
                'customer_phone': booking.customer.phone1,
            }

            data_to_display[booking.id] = booking_data

        # Serialize the booked_slots to JSON format
        booked_slots_json = json.dumps(booked_slots, cls=DjangoJSONEncoder)

        return render(request, 'editbooking.html', {
            'data_to_display1': data_to_display,
            'customer': customer,
            'booked_slots_json': booked_slots_json
        })

    else:
        return render(request, 'mybooking.html')
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'GET':
        booking.delete()  # This will also delete all related BookingDate records
        messages.success(request, 'Booking and related dates have been successfully deleted.')
        return redirect('bookview')  # Replace with the URL where you want to redirect after deletion
    
# views.py
import cv2
import os
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Initialize the camera globally, but don't open it until needed
cap = None

# Load pre-trained face detection model from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def generate_frames():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)  # Initialize the camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if len(faces) > 1:
            cv2.putText(frame, "Multiple Faces Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        elif len(faces) == 1:
            cv2.putText(frame, "Single Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def camera_feed(request):
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)  # Initialize the camera if it's not opened
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def capture_photo(request):
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)  # Initialize the camera if it's not opened
    
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 1:
            return JsonResponse({'status': 'error', 'message': 'Multiple Faces Detected. Photo not captured.'})
        elif len(faces) == 1:
            image_name = 'employee4.jpg'
            image_path = os.path.join(settings.BASE_DIR, 'customerlogin/static/images/', image_name)
            cv2.imwrite(image_path, frame)  # Save without drawing rectangle

            fs = FileSystemStorage(location='customerlogin/static/images/')
            with open(image_path, 'rb') as f:
                photo = ContentFile(f.read(), image_name)
            
            customer = request.user
            employee = get_object_or_404(Customer, email=customer)

            if employee:
                filename = fs.save(image_name, photo)
                employee.photo = f'images/{filename}'
                employee.save()
                cap.release()  # Release the camera
                messages.success(request, 'Your profile picture has been updated successfully!')
                return JsonResponse({'status': 'success', 'message': 'Photo captured and saved successfully!'})
            else:
                cap.release()  # Release the camera
                return JsonResponse({'status': 'error', 'message': 'Employee not found.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No Face Detected. Photo not captured.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to capture image.'})

def camera_page(request):
    return render(request, 'camera_page.html')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # If you want to generate PDF
from io import BytesIO 
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
 # Adjust import paths as necessary


def payment_receipt(request, payment_id):
    if request.session.get('login') == 'yes':
        customer = request.user
        
        # Fetch the payment details based on the given payment_id and ensure it belongs to the customer
        payment = get_object_or_404(payments, booking_id=payment_id, booking_id__customer=customer)
          
        # Fetch the related booking using the correct foreign key relationship
        booking = payment.booking_id
        
        # Fetch the related service provider and service instance
        provider = booking.service_provider
        service_instance = get_object_or_404(service, id=provider.service_table)  # Ensure correct service relation
        
        # Fetch related BookingDate instances
        booking_dates = BookingDate.objects.filter(booking=booking)
        
        # Fetch related Accessoriesbuy instances
        accessories = Accessoriesbuy.objects.filter(Booking1=booking)

        # Group booking dates and time slots
        date_slots = []
        for booking_date in booking_dates:
            date_slots.append({
                'service_start_date': date_format(booking_date.service_start_date, 'd M Y'),  # Format the date
                'time_slot': booking_date.time_slot,
            })
        if booking_date.time_slot=="fullday":
            amount=int(provider.Service_Provider_amountdefalult)+int(provider.Service_Provider_amountdefalult)
        else:
            amount=int(provider.Service_Provider_amountdefalult)

      

        # Prepare accessories details
        accessories_data = []
        for accessory in accessories:
            accessories_data.append({
                'additional_amount': accessory.Additionalaccessoriesamount,
                'total': booking.amount,
                'proof_image': accessory.proofupdate.url if accessory.proofupdate else None,
                'update_date': date_format(accessory.update_date, 'd M Y'),
            })
        
        # Prepare booking details
        booking_data = {
            'booking_id': booking.id,
            'address': booking.customer.address,
            'notes': booking.notes,
            'amount':amount,
            'status': booking.status,
            'date_slots': date_slots,
            'paymentstatus': payment.status,
            'service_provider_name': provider.service_provider_name,
            'service_provider_email': provider.Service_Provider_Email,
            'service_provider_phone': provider.Service_Provider_Phone,
            'service_provider_location': provider.Service_Provider_location,
            'service_name': service_instance.service_name,
            'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
            'customer_email': booking.customer.email,
            'customer_phone': booking.customer.phone1,
            'payment_id': payment.Payment_id,
            'payment_status': payment.status,
            'accessories': accessories_data,  # Include accessories data
        }
        
        print(booking_data)
        
        # Generate PDF (Optional)
        pdf = render_to_pdf('receipt_template_payment.html', booking_data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Receipt_{payment_id}.pdf"
            content = f"inline; filename={filename}"  # Use 'inline' for inline display in browser, 'attachment' to force download
            response['Content-Disposition'] = content
            return response

        # If PDF generation fails, render the HTML template instead
        return render(request, 'receipt_template_payment.html', booking_data)
    
    else:
        return render(request, 'login1.html')


# views.py

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import ChatForm  # Make sure you have a form for handling the chat messages
from .utils import get_bot_response  # Assuming you have a utility function to get bot responses



from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Message, Customer

def chat_view(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        
        if message_content:
            recipient = Customer.objects.get(email='mathew@gmail.com')
            message = Message.objects.create(sender=request.user, recipient=recipient, content=message_content)
            return redirect('chat_view')  
    
    messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('timestamp')

    context = {
        'messages': messages,
        'customer': request.user,
    }
    return render(request, 'chat.html', context)

def fetch_messages(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('timestamp')

    # Prepare message data for JSON response
    message_data = [{
        'content': message.content,
        'is_admin': message.sender.email == 'mathew@gmail.com'
    } for message in messages]

    return JsonResponse({'messages': message_data})
