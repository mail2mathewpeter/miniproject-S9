from django.urls import path
from . import views
app_name = 'employee'
urlpatterns = [
    # path('<str:name>/', views.index1, name='index1'),
    path('', views.index1, name='index1'),
    path('displayuser1/', views.displayuser1, name='displayuser1'),
    path('addservice1/', views.addservice1, name='addservice1'),
    path('addservicesubmit/', views.addservicesubmit, name='addservicesubmit'),
    path('addserviceproviderdata/', views.addserviceproviderdata, name='addserviceproviderdata'),
     path('displayserviceproviderdata1/', views.displayserviceproviderdata1, name='displayserviceproviderdata1'),
    path('addserviceprovider/', views.addserviceprovider, name='addserviceprovider'),
    path('updateservicedata/<int:service_id>/', views.updateservicedata, name='updateservicedata'),
    path('displayservice/', views.displayservice, name='displayservice'),
   path('deleteservice/<int:service_id>/', views.delete_service, name='deleteservice'),
   path('editservice/<int:service_id>/', views.edit_service, name='editservice'),
    path('displayservice/', views.display_service, name='displayservice'),
    path('changeserviceproviderstatus1/<int:service_id>/', views.changeserviceproviderstatus1, name='changeserviceproviderstatus1'),
        path('editserviceproviderdata/<int:service_id>/', views.changeserviceproviderstatus1, name='changeserviceproviderstatus1'),
]
    
    
