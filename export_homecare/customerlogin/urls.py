from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
      path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login1/', views.login1, name='login1'),
     path('service1/', views.service1, name='service1'),
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
    path('error/', views.custom_error_view, name='your_custom_error_view'),
  path('validate_email/', views.validate_email, name='validate_email'),
    path('logout/', views.logout_view, name='logout'),
          path('verify_otp1emailset/', views.verify_otp1emailset, name='verify_otp1emailset'),
         

 path('emailverify/', views.emailverify, name='emailverify'),



    #    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]