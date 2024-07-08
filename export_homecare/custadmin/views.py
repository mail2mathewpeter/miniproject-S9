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
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your views here.

def index(request):
    return render(request, 'adminindex.html')
def editemployee(request,email):
    employee = Employee.objects.get(email=email)
    print(employee);
    
    return render(request, 'editemployee.html', {'data_to_display': employee})

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




def employeedisplay(request):
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
            'photo': customer.photo,
            'status': customer.status,
        }
          data_to_display.append(customer_data)
    return render(request, 'employeedisplay.html', {'data_to_display': data_to_display})

def addemployee(request):
    return render(request, 'adminemployee.html')
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

    return redirect('displayuser')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
 # Import your Customer model here

@csrf_exempt
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
      
        
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

        # Save the file
        fs = FileSystemStorage(location='static/images/')
        filename = fs.save(file.name, file)

        # Create a new employee record
        employee = Employee(
            name=name,
            address=address,
            email=email,
            phone=phone,
            gender=gender,
            designation=designation,
            experience=experience,
            photo=f'images/{filename}'
        )
        employee.save()

        return redirect('index')  # Redirect to a view that lists employees or a success page
    else:
        return render(request, 'adminemployee.html')  # Render the form template
def disableemployee(request, email):
    try:
        customer = Employee.objects.get(email=email)
        print(customer)
        if customer.status == '1':  # Assuming 1 means active and 0 means inactive
            customer.status = 0
            customer.save()
            messages.success(request, f'{customer.name}\'s account has been deactivated.')
        else:
            customer.status = 1
            customer.save()
            messages.success(request, f'{customer.name} \'s account has been activated.')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found.')

    return redirect('employeedisplay')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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

        # Update employee fields
        employee.name = name
        employee.address = address
        employee.email = email
        employee.phone = phone
        employee.gender = gender
        employee.designation = designation
        employee.experience = experience

        # Handle file upload
        if file:
            fs = FileSystemStorage(location='customerlogin/static/images/')
            filename = fs.save(file.name, file)
            employee.photo = f'images/{filename}'

        # Save the updated employee object
        employee.save()
        messages.success(request, 'Employee data updated successfully!')
        return redirect('employeedisplay')  # Adjust the redirect as needed

    return render(request, 'update_employee.html', {'data_to_display': employee})
