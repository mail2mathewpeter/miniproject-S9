from django.shortcuts import render
from django .contrib.auth.models import User
from django.shortcuts import render,redirect
from django .http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from .models import Customer  # Import your Customer model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash
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

def register(request):
    return render(request,'register.html')

def login1(request):
    return render(request, 'login1.html')

def home(request):
    return render(request, 'index.html')


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

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['username']
        try:
            user = Customer.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='1234567890')
            request.session['otp'] = otp # Store OTP in session for verification
            request.session['email'] = email  
            send_otp_email(user.email, otp)
            return render(request, 'verify_otp.html')
        except Customer.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return render(request, 'forgotpassword.html')
    return render(request, 'forgotpassword.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session.get('otp'):
            return render(request, 'change_password.html')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html', {'error': 'Invalid OTP. Please try again.'})
   


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
        gender = request.POST['gender']
        phone1 = request.POST['phone1']
        email = request.POST['email']
        passw = request.POST['pass']
        cpass = request.POST['cpass']
        file = request.FILES['file']

        if passw != cpass:
            return HttpResponse("Passwords do not match")

        # Save the file
        hashed_password = make_password(passw)
       
        fs = FileSystemStorage(location=f'customerlogin/static/images/')
        filename = fs.save(file.name, file)
        # Create a new customer record
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone1=phone1,
            email=email,
            password=hashed_password,  # You might want to hash this before saving
            photo=f'images/{filename}'
        )
        customer.save()

        return render(request, 'home.html') # Redirect to a success page
    else:
        return render(request, 'register.html')
    

  




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
        gender = request.POST['gender']
        phone1 = request.POST['phone1']
        filenotupdate = request.POST['file1']
        

        
      
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

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('useraccount')  # Redirect to a success page
   

    return render(request, 'editaccount.html', {'customer': customer})

def deactivefunctionuser(request):
  if request.method == 'POST':
        customer = request.user
        request.user.is_active = False
        request.user.save()
        messages.success(request, 'Your account has been deactivated.')
        return redirect('login1')  # Redirect to a safe place, e.g., home page
  else:
    return render(request, 'useraccount')
def logincustomer(request):
    if request.method == 'POST':
        # email = "mail2mathewpeter@gmail.com"
        email = request.POST['email']
        password = request.POST['password']
        # password="Mathew@2001"
        user = authenticate(request, email=email, password=password)
        print(f"Username entered: {email}")
        print(f"Password entered: {password}")
        
        if user is not None:
            # Login successful
            login(request, user)
            # Fetch customer details directly from the authenticated user
            try:
                customer1 = Customer.objects.get(email=user.email)
                return render(request, 'userloginhome.html', {'customer': customer1})
            except Customer.DoesNotExist:
                # Handle case where Customer record doesn't exist for the user
                return HttpResponse("Customer record not found.")
        else:
            # Authentication failed
            return render(request, 'login1.html', {'error': 'Invalid credentials'})
    
    return HttpResponse("GET request received. POST request expected.")