from django.shortcuts import render
from customerlogin.models import Customer,BookingDate,Booking; 
from employee.models import service,service_provider; 
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
from .models import Policy  # Import the Policy model
from django.utils import timezone

# Create your views here.
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index5(request):
    if request.session.get('login') == 'customersupport':
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
        return render(request, 'customersupportindex.html', {
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
def customersupporteaccount(request):
    if request.session.get('login') == 'customersupport':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        print(employee)
 # Get the logged-in user
        return render(request, 'accountview5.html', {'customer': employee})
    else:
     return render(request, 'login1.html')

def editcustomerdata(request):
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
        return redirect('customersupport:customersupporteaccount')  # Redirect to a success page
   
   
    return render(request, 'editaccount5.html', {'customer': employee})

def editaccountcustomersupport(request):
    
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
      # Get the logged-in user
    return render(request, 'editaccount5.html', {'customer': employee})


def updatepassword2(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        password = request.POST['password']
       

            # Update the customer record
        
        employee.password = password
        
       
        employee.save()

        messages.success(request, 'Your account password has been updated successfully!')
        return redirect('customersupport:customersupporteaccount') # Redirect to a success page
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def diplaychangepassword(request):
    name=request.session.get('username')
    id=request.session.get('id')
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'changepassword2customersupport.html',{'customer':employee,'id':id})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def displayuser2(request):
   if request.session.get('login') == 'customersupport':
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
        
    return render(request, 'displayusercustomer.html', {'data_to_display': data_to_display1,'customer':employee,'id':id})
   else:
        return render(request, 'login1.html')
   
from customserviceprovider.models import Feedback 

def display_feedback1(request):

    if request.session.get('login') == 'customersupport':
     
        name=request.session.get('username')
        id=request.session.get('id')
   
        employee = get_object_or_404(Employee, id=id)

        # Fetch feedback data from the database, filtering by the logged-in service provider
        feedbacks = Feedback.objects.all() # Adjust the query as needed

        # Pass the data to the template
        context = {
            'data_to_display': feedbacks,
            'messages': request.session.pop('messages', []), 
            'customer': employee,  # Handle messages if any
        }
        print(context)
        return render(request, 'displayfeedback.html', context)
    else:
        return render(request, 'login1.html')  # Redirect to login page

from customerlogin.models import Messageask
def display_message(request):

    if request.session.get('login') == 'customersupport':
     
        name=request.session.get('username')
        id=request.session.get('id')
   
        employee = get_object_or_404(Employee, id=id)

        # Fetch feedback data from the database, filtering by the logged-in service provider
        feedbacks = Messageask.objects.all() # Adjust the query as needed

        # Pass the data to the template
        context = {
            'data_to_display': feedbacks,
            'messages': request.session.pop('messages', []), 
            'customer': employee,  # Handle messages if any
        }
        print(context)
        return render(request, 'displaymessage.html', context)
    else:
        return render(request, 'login1.html')  # Redirect to login page


@cache_control(no_cache=True, no_store=True, must_revalidate=True)   
def add_policy(request):
  if request.session.get('login') == 'customersupport':
     name=request.session.get('username')
     id=request.session.get('id')
   
     employee = get_object_or_404(Employee, id=id)

     return render(request, 'addpolicypage.html', {'customer': employee} )
  else:
        return render(request, 'login1.html')
  


# def viewpolicy(request):

#     if request.session.get('login') == 'customersupport':
     
#         name=request.session.get('username')
#         id=request.session.get('id')
   
#         employee = get_object_or_404(Employee, id=id)

#         # Fetch feedback data from the database, filtering by the logged-in service provider
#         feedbacks = viewpolicy.objects.all() # Adjust the query as needed

#         # Pass the data to the template
#         context = {
#             'data_to_display': feedbacks,
#             'messages': request.session.pop('messages', []), 
#             'customer': employee,  # Handle messages if any
#         }
#         print(context)
#         return render(request, 'viewpolicy.html', context)
#     else:
#         return render(request, 'login1.html')

# View to list all policies
def list_policies(request):
    if request.session.get('login') == 'customersupport':
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        policies = Policy.objects.all()
        return render(request, 'viewpolicy.html', {
            'policies': policies,
            'customer': employee
        })
    else:
        return render(request, 'login1.html')

# View to create a new policy
def create_policy(request):
    if request.method == 'POST':
        name = request.session.get('username')
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        
        # Get form data using the correct field names from the HTML
        policy_name = request.POST['policyName']
        booking_rules = request.POST['bookingRules']
        policy_document = request.FILES['policyImage']  # Note: using FILES for file upload
        
        # Create a new Policy instance
        new_policy = Policy(
            Company_Policy=policy_name,
            booking_rules=booking_rules,
            upload_document=policy_document,
            employee_id=employee,  # Direct assignment of employee object
            date=timezone.now()  # Automatically set current date
        )
        new_policy.save()

        messages.success(request, 'Company Policy added successfully!')
        return redirect('customersupport:list_policies')  # Adjust redirect URL as needed

    return render(request, 'addpolicypage.html')

def edit_policy(request, policy_id):
    if request.session.get('login') == 'customersupport':
        id = request.session.get('id')
        employee = get_object_or_404(Employee, id=id)
        policy = get_object_or_404(Policy, id=policy_id)

        if request.method == 'POST':
            # Update policy with form data
            policy.Company_Policy = request.POST['policyName']
            policy.booking_rules = request.POST['bookingRules']
            
            # Handle file upload if a new file is provided
            if 'policyImage' in request.FILES:
                policy.upload_document = request.FILES['policyImage']
            
            policy.date = timezone.now()
            policy.save()
            
            messages.success(request, 'Policy updated successfully!')
            return redirect('customersupport:list_policies')

        return render(request, 'editpolicypage.html', {
            'policy': policy,
            'customer': employee
        })
    else:
        return render(request, 'login1.html')

def enable_disable_policy(request, policy_id):
    if request.session.get('login') == 'customersupport':
        policy = get_object_or_404(Policy, id=policy_id)
        if policy.status=="disabled":
            policy.status="enabled"
            messages.success(request, f'Policy has been  successfully Activated!')
        else:
            policy.status="disabled"
            messages.success(request, f'Policy has been  successfully Deactivate!')
        policy.save()
        
        
        return redirect('customersupport:list_policies')

    else:
        return render(request, 'login1.html')

from customer_support.models import Policy 
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def policypdf(request):
    if request.session.get('login') == 'customersupport':
        # Fetch all policies
        policy_list = Policy.objects.all().order_by('-date')

        policy_details = []

        for policy in policy_list:
            employee = policy.employee_id  # Get the related employee

            policy_detail = {
                'policy_id': policy.id,
                'company_policy': policy.Company_Policy,
                'booking_rules': policy.booking_rules,
                'upload_document': policy.upload_document,
                'date': policy.date,
                'status': policy.status,
                'employee_name': employee.name,  # Assuming employee has a name field
                'employee_email': employee.email,  # Assuming employee has an email field
                'employee_designation': employee.designation  # Assuming employee has a designation field
            }

            policy_details.append(policy_detail)

        # Prepare the context
        context = {
            'policy_details': policy_details,
            'current_year': timezone.now().year,
        }

        return render(request, 'policypdf.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')

 
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def feedback1pdf(request):
    if request.session.get('login') == 'customersupport':
        # Fetch all policies
        policy_list = Feedback.objects.all()
        print(policy_list)

        policy_details = []

        for policy in policy_list:
           # Get the related employee

            policy_detail = {
                'customer': policy.customer,
                'serviceprovider': policy.serviceprovider,
                'service_received': policy.service_received,
                
                'rating': policy.rating,
                'experience': policy.experience,
                'status': policy.status,
                'suggestions': policy.suggestions,  # Assuming employee has a name field
                  # Assuming employee has an email field
                
            }

            policy_details.append(policy_detail)

        # Prepare the context
        context = {
            'policy_details': policy_details,
            'current_year': timezone.now().year,
        }

        return render(request, 'feedback1pdf.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')
    
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def queriespdf(request):
    if request.session.get('login') == 'customersupport':
        # Fetch all policies
        feedbacks = Messageask.objects.all() # Adjust the query as needed

        # Pass the data to the template
        context = {
            'data_to_display': feedbacks,
            'messages': request.session.pop('messages', []), 
             # Handle messages if any
        }
        print(context)

        # Prepare the context
       

        return render(request, 'queriespdf.html', context)
    else:
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')

