from django.urls import path
from . import views
app_name = 'admin1'
urlpatterns = [
    path('', views.index, name='index'),
    path('displayuser/', views.displayuser, name='displayuser'),
     path('displayserviceadmin/', views.displayserviceadmin, name='displayserviceadmin'),
     path('displayserviceprovideradmin/', views.displayserviceprovideradmin, name='displayserviceprovideradmin'),
     path('addemployee/', views.addemployee, name='addemployee'),
     path('addemployeedata/', views.registeremployee, name='addemployeedata'),
     path('employeedisplay/', views.employeedisplay, name='employeedisplay'),
       path('serviceproviderdisplay/', views.serviceproviderdisplay, name='serviceproviderdisplay'),
    # path('displayuserfull/', views.displayuserfull, name='displayuserfull'),
path('editemployee/<str:email>/', views.editemployee, name='editemployee'),
 path('changeuserstatus/<str:email>/', views.changeuserstatus, name='changeuserstatus'),
 path('editemployeeupdate/<str:email>/', views.editemployeeupdate, name='editemployeeupdate'),
  path('disableemployee/<str:email>/', views.disableemployee, name='disableemployee'),
    path('validate_email/', views.validate_email, name='validate_email'),
        path('admin1/passwordaddemployee/<str:email>/', views.passwordaddemployee, name='passwordaddemployee'),
      path('employeepasswordadd/<str:email>/', views.employeepasswordadd, name='employeepasswordadd'),
        path('changeserviceproviderstatus2/<int:service_id>/', views.changeserviceproviderstatus2, name='changeserviceproviderstatus2'),
    # path('employeepasswordadd/<str:email>/', views.employeepasswordadd, name='employeepasswordadd'),
      
]