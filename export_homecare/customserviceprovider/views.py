from django.shortcuts import render
from django.shortcuts import render
from customerlogin.models import Customer,BookingDate,Booking; 
from employee.models import service,service_provider;
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash   
from django.contrib import messages 
from django.shortcuts import render
from django.utils import timezone
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
from .models import Accessoriesbuy
from django.shortcuts import render, redirect

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index2(request):
     if request.session.get('login') == 'serviceprovider':
        id = request.session.get('id')
      
        employee = get_object_or_404(service_provider, id=id)
        serviceprovideramount = employee.Service_Provider_amountdefalult
        bookings = Booking.objects.filter(Q(status="Approved")  | Q(status="pending"))
        pending_approval = bookings.count()
        
        filtered_bookings = []

       
        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)

            # Filter bookings based on service provider
            if provider.id == employee.id:
                # Fetch related BookingDate instances and sort by date in descending order
                booking_dates = BookingDate.objects.filter(booking=booking).order_by('-service_start_date')
                
                # Initialize variables for Accessoriesbuy
                Accessoriesbuy_amount = None
                Accessoriesbuy_proof = None
                
                # Attempt to fetch Accessoriesbuy instance
                try:
                    Accessoriesbuy1 = Accessoriesbuy.objects.get(Booking1=booking)
                    Accessoriesbuy_amount = Accessoriesbuy1.Additionalaccessoriesamount
                    Accessoriesbuy_proof = Accessoriesbuy1.proofupdate
                except Accessoriesbuy.DoesNotExist:
                    # If Accessoriesbuy instance does not exist, handle it here
                    Accessoriesbuy_amount = None
                    Accessoriesbuy_proof = None

                # Create a dictionary of booking data
                dates_and_slots = [{'date': bd.service_start_date, 'slot': bd.time_slot} for bd in booking_dates]

                # Count the number of unique dates
                unique_dates = len(set(bd['date'] for bd in dates_and_slots))

                # Determine if the last slot is "FULL_DAY"
                last_slot_is_full_day = dates_and_slots[-1]['slot'] == 'fullday' if dates_and_slots else False

                booking_data = {
                    'booking_id': booking.id,
                    'address': booking.address,
                    'notes': booking.notes,
                    'status': booking.status,
                    'amount': booking.amount,
                    'serviceprovideramount': serviceprovideramount,
                    'Accessoriesbuyamount': Accessoriesbuy_amount,
                    'Accessoriesbuyamountproof': Accessoriesbuy_proof,
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
                    'photo': booking.customer.photo,
                    'dates_and_slots': dates_and_slots,
                    'number_of_dates': unique_dates,
                    'last_slot_is_full_day': last_slot_is_full_day,
                }

                filtered_bookings.append(booking_data)

        # Sort filtered_bookings by the earliest date in 'dates_and_slots' in descending order
        sorted_bookings = sorted(filtered_bookings, key=lambda b: min(d['date'] for d in b['dates_and_slots']), reverse=True)

        # Render the template with the sorted bookings
        bookings = Booking.objects.filter(
        Q(status="Solved"),
        service_provider=employee
    )
      

    # Calculate the total amount from these bookings
        total_amount = bookings.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_bookings = bookings.count()
#         now = timezone.now()

# # Calculate the date one month ago
#         one_month_ago = now - timedelta(days=30)

# # Filter the customers who joined in the last month
#         total_customers_last_month = Customer.objects.filter(date_joined__gte=one_month_ago).count()
    
        total_customers = Customer.objects.filter(is_staff=False, is_superuser=False).count()
        return render(request, 'serviceproviderindex.html', {'data_to_display': sorted_bookings, 'customer': employee, 'id': id,'total_amount': total_amount, 'total_bookings': total_bookings,'pending_approval':pending_approval,'total_customers':total_customers})
     else:
         return render(request, 'login1.html')
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bookeduserdetails(request):
    if request.session.get('login') == 'serviceprovider':
        id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=id)
        
        serviceprovideramount = employee.Service_Provider_amountdefalult

        # Filter bookings with status "Approved", "Solved", or "Pending"
        bookings = Booking.objects.filter(Q(status="Approved") | Q(status="Solved") | Q(status="pending"))
        
        filtered_bookings = []

        for booking in bookings:
            provider = booking.service_provider
            service1 = provider.service_table
            service2 = get_object_or_404(service, id=service1)

            # Filter bookings based on service provider
            if provider.id == employee.id:
                # Fetch related BookingDate instances and sort by date in descending order
                booking_dates = BookingDate.objects.filter(booking=booking).order_by('-service_start_date')
                
                # Initialize variables for Accessoriesbuy
                Accessoriesbuy_amount = None
                Accessoriesbuy_proof = None
                
                # Attempt to fetch Accessoriesbuy instance
                try:
                    Accessoriesbuy1 = Accessoriesbuy.objects.get(Booking1=booking)
                    Accessoriesbuy_amount = Accessoriesbuy1.Additionalaccessoriesamount
                    Accessoriesbuy_proof = Accessoriesbuy1.proofupdate
                except Accessoriesbuy.DoesNotExist:
                    # If Accessoriesbuy instance does not exist, handle it here
                    Accessoriesbuy_amount = None
                    Accessoriesbuy_proof = None

                # Create a dictionary of booking data
                dates_and_slots = [{'date': bd.service_start_date, 'slot': bd.time_slot} for bd in booking_dates]

                # Count the number of unique dates
                unique_dates = len(set(bd['date'] for bd in dates_and_slots))

                # Determine if the last slot is "FULL_DAY"
                last_slot_is_full_day = dates_and_slots[-1]['slot'] == 'fullday' if dates_and_slots else False

                booking_data = {
                    'booking_id': booking.id,
                    'address': booking.address,
                    'notes': booking.notes,
                    'status': booking.status,
                    'amount': booking.amount,
                    'serviceprovideramount': serviceprovideramount,
                    'Accessoriesbuyamount': Accessoriesbuy_amount,
                    'Accessoriesbuyamountproof': Accessoriesbuy_proof,
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
                    'photo': booking.customer.photo,
                    'dates_and_slots': dates_and_slots,
                    'number_of_dates': unique_dates,
                    'last_slot_is_full_day': last_slot_is_full_day,
                }

                filtered_bookings.append(booking_data)

        # Sort filtered_bookings by the earliest date in 'dates_and_slots' in descending order
        sorted_bookings = sorted(filtered_bookings, key=lambda b: min(d['date'] for d in b['dates_and_slots']), reverse=True)

        # Render the template with the sorted bookings
        return render(request, 'bookeduserdetails.html', {'data_to_display': sorted_bookings, 'customer': employee, 'id': id})
    
    else:
        return render(request, 'login1.html')



# def update_values(request):
#     additional_amount = request.POST.get('value1')
#     file = request.FILES.get('file')
#     basicsalary = request.POST.get('basic')
#     number_of_dates = request.POST.get('number_of_dates')
#     last_slot_is_full_day = request.POST.get('last_slot_is_full_day')
#     bookingid = request.POST.get('bookingid') 
#     print(bookingid) # Add this to your form if needed
#     instance = Booking.objects.get(id=bookingid)
#     timezone1= timezone.now()
#     print(last_slot_is_full_day)
#     # Update the instance with new values
#     if last_slot_is_full_day:
#         instance.amount = int(additional_amount)+((int(basicsalary)+int(basicsalary))*int(number_of_dates))
#     else:
#         instance.amount = int(additional_amount)+(int(basicsalary)*int(number_of_dates))
#     instance.status="Solved"
#     instance.paymentstatus="Notdone"
#     filename = None  
#     if file:
#                 fs = FileSystemStorage(location='customerlogin/static/images/')
#                 filename = fs.save(file.name, file)
               
#     customer = Accessoriesbuy(
#             Booking1=instance,
#             Additionalaccessoriesamount=additional_amount,
#             proofupdate= f'images/{filename}',
#             update_date=timezone1,
   
#         )
#     customer.save()
#     instance.save()
#     email=instance.customer.email
#     name=instance.customer.first_name
#     feedback1(str(email)) 
#     messages.success(request, 'Additional accessories amount has been successfully added!')

#     return redirect('customserviceprovider:bookeduserdetails')




def update_values(request):
    additional_amount = request.POST.get('value1')
    file = request.FILES.get('file')
    basicsalary = request.POST.get('basic')
    number_of_dates = request.POST.get('number_of_dates')
    last_slot_is_full_day = request.POST.get('last_slot_is_full_day')
    bookingid = request.POST.get('bookingid') 

    print(bookingid) # Add this to your form if needed
    instance = Booking.objects.get(id=bookingid)
    provider = instance.service_provider
    service_instance = get_object_or_404(service, id=provider.service_table)  
    timezone1 = timezone.now()
    service1=service_instance.service_name
    print(last_slot_is_full_day)

    # Update the instance with new values
    if last_slot_is_full_day:
        instance.amount = int(additional_amount) + ((int(basicsalary) + int(basicsalary)) * int(number_of_dates))
    else:
        instance.amount = int(additional_amount) + (int(basicsalary) * int(number_of_dates))
    
    instance.status = "Solved"
    instance.paymentstatus = "Notdone"

    filename = None  
    if file:
        fs = FileSystemStorage(location='customerlogin/static/images/')
        filename = fs.save(file.name, file)
               
    customer = Accessoriesbuy(
        Booking1=instance,
        Additionalaccessoriesamount=additional_amount,
        proofupdate=f'images/{filename}',
        update_date=timezone1,
    )
    customer.save()
    email = instance.customer.email
    name = instance.customer.first_name + " " + instance.customer.last_name
    
    instance.save()

    # Fetch email and name

    request.session["status"] = "done"

    # Pass the correct arguments to the feedback1 function
    feedback2(request,email,name,service1,provider) 
    
    messages.success(request, 'Additional accessories amount has been successfully added!')

    return redirect('customserviceprovider:bookeduserdetails')
def feedback2(request,email,name,service_name,provider):
    print(name)
    print(email)
    request.session["service"] = service_name
    request.session["email"] = email
    request.session["name"] = name
    request.session["serviceprovier_id"] = provider.id
    
    subject = 'Your booked service has been successfully solved'
    message = (
        f"Hello, {name}\n\n"
        f"Thank you for using our service. We would appreciate it if you could provide us feedback about your experience.\n\n"
        f"Please click the link below to submit your feedback:\n\n"
        f"http://127.0.0.1:8000/customserviceprovider/feedback1\n\n"
        f"Best regards,\n"
        f"The Expert Homecare Team"
    )
    
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

def serviceproviderpasswordadd(request,email):
        
    return render(request, 'servicproviderchangepassword.html',{'email':email})


def passwordaddserviceprovider(request, email):
    if request.method == 'POST':
       employee = get_object_or_404(service_provider, Service_Provider_Email=email)
       password = request.POST.get('password')
      # hashed_password = make_password(password)
       employee.status="4"
       employee.password=password
       employee.save()
       messages.success(request, 'Serviceprovider password updated Successfully.Please login with new credentials')
       return redirect('login1')
    
def logoutserviceprovider(request):
    request.session['login'] = " "
    request.session['id'] = " "
    
    # Redirect to a success page or login page
    return redirect('login1')

def changebookingstatus1(request,booking_id):
    if request.method == 'GET':
        id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=id)
        update = get_object_or_404(Booking, id=booking_id)
        update.status="Approved"
        update.save();

        messages.success(request, 'Service has been successfully Approved!')
        return redirect('customserviceprovider:bookeduserdetails')# Redirect to a success page
   

    return render(request, 'changepassword.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editaccountserviceprovider(request):
    if request.session.get('login') == 'serviceprovider':
       name=request.session.get('username')
       id=request.session.get('id')
       employee = get_object_or_404(service_provider, id=id)
       print(employee.service_provider_name)
      # Get the logged-in user
       return render(request, 'editaccount5.html', {'customer': employee})
    else:
      return render(request, 'login1.html')
def serviceprovideraccount(request):
     if request.session.get('login') == 'serviceprovider':
       name=request.session.get('username')
       id=request.session.get('id')
    
       employee = get_object_or_404(service_provider, id=id)
       print(employee)
 # Get the logged-in user
       return render(request, 'accountview5.html',{'customer': employee})
     else:
      return render(request, 'login1.html')
     
def editemployeedata4(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
    
        employee1 = get_object_or_404(service_provider, id=id)
        
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
                employee1.photo = f'images/{filename}'


            # Update the customer record
    
        employee1.service_provider_name = first_name
        employee1.Service_Provider_Address = last_name
        employee1.Service_Provider_Phone = phone
        employee1.Service_Provider_Experience = experience
        employee1.Service_Provider_gender = gender
        employee1.save()


        messages.success(request, 'Your profile details has been updated successfully!')
        return redirect('customserviceprovider:serviceprovideraccount')  # Redirect to a success page
   
   
    return render(request, 'customserviceprovider:accountview5.html')

def changepassword(request):
    if request.method == 'POST':
        name=request.session.get('username')
        id=request.session.get('id')
        employee = get_object_or_404(service_provider, id=id)
        password = request.POST['password']
       

            # Update the customer record
        
        employee.password = password
    
       
        employee.save()

        messages.success(request, 'Your account password has been updated successfully!')
        return redirect('customserviceprovider:serviceprovideraccount') # Redirect to a success page
def changepasswordaccountview(request):
     if request.session.get('login') == 'serviceprovider':
        id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=id)
        print(employee.service_provider_name)
      # Get the logged-in user
        return render(request, 'changepasswordserviceprovider.html', {'customer': employee})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
  # Ensure all models are correctly imported
from django.db.models import Count

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages

def viewbookingpdfserviceprovider(request):
    if request.session.get('login') == 'serviceprovider':
        # Get the logged-in employee's ID from the session
        emp_id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=emp_id)

        # Fetch bookings associated with this specific service provider
        bookings = Booking.objects.filter(service_provider=employee)

        # Prepare provider data
        provider_info = {
            'service_provider_name': employee.service_provider_name,
            'service_provider_email': employee.Service_Provider_Email,
            'service_provider_phone': employee.Service_Provider_Phone,
            'service_provider_address': employee.Service_Provider_Address,
            'service_provider_gender': employee.Service_Provider_gender,
            'service_provider_experience': employee.Service_Provider_Experience,
            'service_provider_location': employee.Service_Provider_location,
            'num_bookings': bookings.count(),
            'bookings': []  # Placeholder for booking details
        }

        # Prepare booking details
        for booking in bookings:
            booking_data = {
                'id': booking.id,
                'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                'address': booking.address,
                'booking_date': booking.booking_date.date(),
                'amount': booking.amount,
                'status': booking.status,
                'email': booking.customer.email,
                'phone': booking.customer.phone1,
                'gender': booking.customer.gender,
                'photo': booking.customer.photo.url if booking.customer.photo else None,
            }
            provider_info['bookings'].append(booking_data)  # Add booking data to provider info

        # Prepare the context
        context = {
            'service_providers': [provider_info],  # Wrap in a list for consistency
            'current_year': timezone.now().year,
        }

        return render(request, 'serviceproviderbookingpdf.html', context)

    # Redirect to login page if not logged in
    messages.error(request, 'Please login to access this page.')
    return redirect('login1')

def feedback1(request):
        service_name = request.session.get("service") 
        Customeremail = request.session.get("email") 
        name = request.session.get("name") 
        serviceprovier = request.session.get("serviceprovier_id") 
        status = request.session.get("status") 
        print(name)
        print(Customeremail)
        if status =="done":
           return render(request, 'feedback.html',{'service':service_name,'Customeremail':Customeremail,'name':name,'serviceprovier':serviceprovier})
        else:
             return render(request, 'feedbackclose.html')

from .models import Feedback 
def feedback_view(request):
    if request.method == 'POST':
        customer_email = request.POST.get('email')
        service_provider_id = request.POST.get('serviceprovier')  # service provider ID from the form
        service = request.POST.get('service')
        print(service)
        rating = request.POST.get('rating')
        experience = request.POST.get('experience')
        improve = request.POST.get('improve')
        request.session["status"] = "No"

        # Get the customer instance
        customer = Customer.objects.get(email=customer_email)  # Adjust if needed

        # Fetch the service provider instance using the ID
        service_provider1 = service_provider.objects.get(id=service_provider_id)

        # Save feedback to the database
        Feedback.objects.create(
            customer=customer,
            serviceprovider=service_provider1,  # Use the actual service provider instance
            service_received=service,
            rating=rating,
            experience=experience,
            suggestions=improve,
            status=1
        )

        return render(request, 'feedbackclose.html')


    
def display_feedback(request):
    # Check if the user is logged in as a service provider
    if request.session.get('login') == 'serviceprovider':
        # Get the logged-in employee's ID from the session
        emp_id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=emp_id)

        # Fetch feedback data from the database, filtering by the logged-in service provider
        data_to_display = Feedback.objects.filter(serviceprovider=employee)  # Adjust the query as needed

        # Pass the data to the template
        context = {
            'data_to_display': data_to_display,
            'messages': request.session.pop('messages', []), 
            'customer': employee,  # Handle messages if any
        }
        print(context)
        return render(request, 'displayfeedback.html', context)
    else:
        return render(request, 'login1.html')



def feedback_close(request):
    return render(request, 'feedbackclose.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from .models import Feedback, service_provider

def feedbackpdf(request):
    if request.session.get('login') == 'serviceprovider':
        # Get the logged-in service provider's ID
        emp_id = request.session.get('id')
        employee = get_object_or_404(service_provider, id=emp_id)

        # Fetch all feedback for the logged-in service provider, ordered by latest date
        feedback_list = Feedback.objects.filter(serviceprovider=employee).order_by('-created_at')

        feedback_details = []

        for feedback in feedback_list:
            # Store feedback details
            feedback_detail = {
                'customer_name': f"{feedback.customer.first_name} {feedback.customer.last_name}",
                'service_received': feedback.service_received,
                'rating': feedback.rating,
                'experience': feedback.experience,
                'suggestions': feedback.suggestions or 'No suggestions',
             
                'feedback_date': feedback.created_at.strftime("%Y-%m-%d"),
            }

            # Append each feedback detail to the list
            feedback_details.append(feedback_detail)

        # Prepare the context to pass to the template
        context = {
            'feedback_details': feedback_details,
            'service_provider': employee,
            'current_year': timezone.now().year,
        }
        print(context)

        # Render the feedback PDF template with the context data
        return render(request, 'feedbackpdf.html', context)

    else:
        # Redirect to login if the user is not logged in as a service provider
        messages.error(request, 'Please login to access this page.')
        return redirect('login1')
