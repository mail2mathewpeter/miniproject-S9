from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from .models import Customer 
from custadmin.models import Employee;
from employee.models import service;   # Import your Customer model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
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

    return render(request,'service.html', {'data_to_display': data_to_display1})

def register(request):
    return render(request,'register.html')

def login1(request):
    return render(request, 'login1.html')

def home(request):
   
      return render(request, 'index.html')
   

def emailverify(request):
    return render(request, 'emailverify.html')


def userloginhome(request):
    
    customer = request.user  # Get the logged-in user
    return render(request, 'userloginhome.html', {'customer': customer})

def useraccount(request):
    customer = request.user  # Get the logged-in user
    return render(request, 'accountview.html', {'customer': customer})
def editaccount(request):
    customer = request.user  # Get the logged-in user
    return render(request, 'editaccount.html', {'customer': customer})
def updatepassword(request):
    customer = request.user  # Get the logged-in user
    return render(request, 'changepassword.html', {'customer': customer})
def deactiveaccountuser(request):
    customer = request.user  # Get the logged-in user
    return render(request, 'deactiveuseraccount.html', {'customer': customer})


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
    message = f'Your OTP Register Email is: {otp}'
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

        messages.success(request, 'Your profile has been updated successfully!')
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

        # messages.success(request, 'Your profile has been updated successfully!')
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
# def logincustomer(request):
#     if request.method == 'POST':
#         # email = "mail2mathewpeter@gmail.com"
#         email = request.POST['email']
#         password = request.POST['password']
#         # password="Mathew@2001"
#         user = authenticate(request, email=email, password=password,status='1')
#         print(f"Username entered: {email}")
#         print(f"Password entered: {password}")
        
#         if user is not None:
#             # Login successful
#             login(request, user)
#             # Fetch customer details directly from the authenticated user
#             try:
#                 customer1 = Customer.objects.get(email=user.email)
#                 return render(request, 'userloginhome.html', {'customer': customer1})
#             except Customer.DoesNotExist:
#                 # Handle case where Customer record doesn't exist for the user
#                 return HttpResponse("Customer record not found.")
#         else:
#             # Authentication failed
#             return render(request, 'login1.html', {'error': 'Invalid credentials'})
    
#     return HttpResponse("GET request received. POST request expected.")

# customerlogin/views.py

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login


def logincustomer(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
       # employee = Employee.objects.get(email='experthomecare43@gmail.com')
        #print(employee)
        # Authenticate user with email, password, and status check ('1' for customers)
        user = authenticate(request, email=email, password=password)
        print(user);
        print(f"Username entered: {email}")
        print(f"Password entered: {password}")
       # print(employee.email)
       # print(employee.password);
        
        if user is not None:
            # Check if the authenticated user is a customer
            try:
                customer = Customer.objects.get(email=user.email)
                login(request, user)
                if(customer.status=='1'):
                    request.session['login'] = 'yes'
                    return redirect("userloginhome") 
                elif(customer.status=='2'):
                    request.session['login'] = 'yes'
                    return redirect('admin1:index') 
                    
                else:
                     messages.success(request, 'Your account is in deactivated mode.')
                     return render(request, 'login1.html')

                
                
            
            except Customer.DoesNotExist:
                # Handle case where Customer record doesn't exist
                return HttpResponse("Customer record not found.")
        
        # elif employee.email==email and employee.password==password and employee.status =='2':
        #     # Authenticate user with email and password only (without status check)
        #     # login(request, user)
        #     name=employee.name;
        #     request.session['username']=name;
        #     request.session['login'] = 'yes'
        #     name=request.session.get('username')
        #     return redirect('employee:index1',{'customer':name}) 
            
            
            
        else:
                # Authentication failed
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return HttpResponse("GET request received. POST request expected.")


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

from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import format as date_format
from .models import Booking, BookingDate, service  # Import the Payment model




# def chat_view(request):
#     if request.method == 'POST':
#         message_content = request.POST.get('message')
        
#         if message_content:
#             recipient = Customer.objects.get(email='mathew@gmail.com')
#             message = Message.objects.create(sender=request.user, recipient=recipient, content=message_content)
#             return redirect('chat_view')  
    
#     messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('timestamp')

#     context = {
#         'messages': messages,
#         'customer': request.user,
#     }
#     return render(request, 'chat.html', context)

