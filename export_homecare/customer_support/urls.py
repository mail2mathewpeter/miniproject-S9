from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'customersupport'
urlpatterns = [
    # path('<str:name>/', views.index1, name='index1'),
    path('', views.index5, name='index5'),

      path('customersupporteaccount', views.customersupporteaccount, name='customersupporteaccount'),
     path('editaccountcustomersupport', views.editaccountcustomersupport, name='editaccountcustomersupport'),
        path('editcustomerdata', views.editcustomerdata, name='editcustomerdata'),
           path('updatepassword2/', views.updatepassword2, name='updatepassword2'),
      path('diplaychangepassword/', views.diplaychangepassword, name='diplaychangepassword'),
         path('displayuser2/', views.displayuser2, name='displayuser2'),
                path('display_feedback1/', views.display_feedback1, name='display_feedback1'),
                    path('display_message/', views.display_message, name='display_message'),
          path('display_message/', views.display_message, name='display_message'),
           path('add_policy/', views.add_policy, name='add_policy'),
           path('policies/', views.list_policies, name='list_policies'),  # URL for listing policies
           path('policies/create/', views.create_policy, name='create_policy'),
           path('edit-policy/<int:policy_id>/', views.edit_policy, name='edit_policy'),
           path('enable_disable_policy/<int:policy_id>/', views.enable_disable_policy, name='enable_disable_policy'),
           path('policy/pdf/', views.policypdf, name='policy_pdf'),
           path('feedback/pdf/', views.feedback1pdf, name='feedback1pdf'),
              path('queries/pdf/', views.queriespdf, name='queriespdf'),
           
           
            
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
