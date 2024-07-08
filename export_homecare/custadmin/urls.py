from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('displayuser/', views.displayuser, name='displayuser'),
     path('addemployee/', views.addemployee, name='addemployee'),
     path('addemployeedata/', views.registeremployee, name='addemployeedata'),
     path('employeedisplay/', views.employeedisplay, name='employeedisplay'),
    
    # path('displayuserfull/', views.displayuserfull, name='displayuserfull'),
path('editemployee/<str:email>/', views.editemployee, name='editemployee'),
 path('changeuserstatus/<str:email>/', views.changeuserstatus, name='changeuserstatus'),
 path('editemployeeupdate/<str:email>/', views.editemployeeupdate, name='editemployeeupdate'),
  path('disableemployee/<str:email>/', views.disableemployee, name='disableemployee'),
 

]