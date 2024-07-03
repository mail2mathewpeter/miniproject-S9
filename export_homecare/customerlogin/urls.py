from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
      path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login1/', views.login1, name='login1'),
      path('registercustomer', views.registercustomer, name='registercustomer'),
      path('logincustomer', views.logincustomer, name='logincustomer'),
      path('forgot', views.forgot, name='forgot'),
       path('forgotpassword', views.forgotpassword, name='forgotpassword'),
     path('verify_otp', views.verify_otp, name='verify_otp'),
      path('change_password', views.change_password, name='change_password'),
       path('userloginhome', views.userloginhome, name='userloginhome'),
       path('useraccount', views.useraccount, name='useraccount'),
       path('editaccount', views.editaccount, name='editaccount'),
       path('updatecustomerdata', views.updatecustomerdata, name='updatecustomerdata'),
        path('changepassworduser', views.changepassworduser, name='changepassworduser'),
       path('updatepassword', views.updatepassword, name='updatepassword'),
      path('deactiveaccountuser', views.deactiveaccountuser, name='deactiveaccountuser'),
          path('deactivefunctionuser', views.deactivefunctionuser, name='deactivefunctionuser'),
      
       
]