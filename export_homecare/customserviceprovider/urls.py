from django.urls import path
from . import views
app_name = 'customserviceprovider'
urlpatterns = [
    path('', views.index2, name='index2'),
    path('bookeduserdetails/', views.bookeduserdetails, name='bookeduserdetails'),
    path('logoutserviceprovider/', views.logoutserviceprovider, name='logoutserviceprovider'),
    path('update-values/', views.update_values, name='update_values'),
    path('serviceproviderpasswordadd/<str:email>/', views.serviceproviderpasswordadd, name='serviceproviderpasswordadd'),
    path('passwordaddserviceprovider/<str:email>/', views.passwordaddserviceprovider, name='passwordaddserviceprovider'),
    path('changebookingstatus1/<int:booking_id>/', views.changebookingstatus1, name='changebookingstatus1'),
    path('editaccountserviceprovider/', views.editaccountserviceprovider, name='editaccountserviceprovider'),
    path('serviceprovideraccount', views.serviceprovideraccount, name='serviceprovideraccount'),
    path('editemployeedata4', views.editemployeedata4, name='editemployeedata4'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('changepasswordaccountview', views.changepasswordaccountview, name='changepasswordaccountview'),
    path('viewbookingpdfserviceprovider', views.viewbookingpdfserviceprovider, name='viewbookingpdfserviceprovider'),
    path('feedback1', views.feedback1, name='feedback1'),
    path('display_feedback', views.display_feedback, name='display_feedback'),
    path('feedback_view', views.feedback_view, name='feedback_view'),
    path('feedback_close', views.feedback_close, name='feedback_close'),
    path('feedbackpdf', views.feedbackpdf, name='feedbackpdf'),
    
    
    
]