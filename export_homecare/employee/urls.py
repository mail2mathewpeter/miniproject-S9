from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employee'
urlpatterns = [
    # path('<str:name>/', views.index1, name='index1'),
    path('', views.index1, name='index1'),
    path('logout1/', views.logout_view1, name='logout1'),
    path('displayuser1/', views.displayuser1, name='displayuser1'),

    path('addservice1/', views.addservice1, name='addservice1'),
    path('employeccount1/', views.employeccount1, name='employeccount1'),
    path('editaccount1', views.editaccount1, name='editaccount1'),
    path('addservicesubmit/', views.addservicesubmit, name='addservicesubmit'),
    path('addserviceproviderdata/', views.addserviceproviderdata, name='addserviceproviderdata'),
     path('displayserviceproviderdata1/', views.displayserviceproviderdata1, name='displayserviceproviderdata1'),
    path('addserviceprovider/', views.addserviceprovider, name='addserviceprovider'),
    path('updateservicedata/<int:service_id>/', views.updateservicedata, name='updateservicedata'),
    path('displayservice/', views.displayservice, name='displayservice'),
   path('deleteservice/<int:service_id>/', views.delete_service, name='deleteservice'),
   path('changeuserstatus2/<str:email>/', views.changeuserstatus2, name='changeuserstatus2'),
   path('editservice/<int:service_id>/', views.edit_service, name='editservice'),
    path('displayservice/', views.display_service, name='displayservice'),
    path('editemployeedata/', views.editemployeedata, name='editemployeedata'),
    path('updatepassword1/', views.updatepassword1, name='updatepassword1'),
      path('diplaychangepassword/', views.diplaychangepassword, name='diplaychangepassword'),
        path('viewbooking/', views.viewbooking, name='viewbooking'),
         path('viewbookingall/', views.viewbooking, name='viewbookingall'),
        
           path('changebookingstatus/<int:booking_id>/', views.changebookingstatus, name='changebookingstatus'),
    path('changeserviceproviderstatus1/<int:service_id>/', views.changeserviceproviderstatus1, name='changeserviceproviderstatus1'),
        path('editserviceproviderdata/<int:id2>/', views.editserviceproviderdata1, name='editserviceproviderdata'),
        path('displayserviceproviderdataeditpage/<int:id1>/', views.displayserviceproviderdataeditpage, name='displayserviceproviderdataeditpage'),
         path('validate_email1/', views.validate_email1, name='validate_email1'),
          # path('validate_email3/', views.validate_email3, name='validate_email3'),
          path('logoutaemployee/', views.logoutaemployee, name='logoutaemployee'),
     path('serviceproviderpdfemployee/', views.serviceproviderpdfemployee, name='serviceproviderpdfemployee'),
    path('viewbookingpdfemployee/', views.viewbookingpdfemployee, name='viewbookingpdfemployee'),
  #  path('validate_image/', views.validate_image, name='validate_image'),
    path('validate_email/', views.validate_email1, name='validate_email'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
