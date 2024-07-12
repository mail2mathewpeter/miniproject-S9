from django.urls import path
from . import views
app_name = 'employee'
urlpatterns = [
    # path('<str:name>/', views.index1, name='index1'),
    path('', views.index1, name='index1'),
    path('displayuser1/', views.displayuser1, name='displayuser1'),
    path('addservice1/', views.addservice1, name='addservice1'),
    path('addservicesubmit/', views.addservicesubmit, name='addservicesubmit'),
    path('displayservice/', views.displayservice, name='displayservice'),
   path('deleteservice/<int:id>/', views.delete_service, name='deleteservice'),
   path('editservice/<int:id>/', views.edit_service, name='editservice'),
    path('displayservice/', views.display_service, name='displayservice'),
]
    
    
