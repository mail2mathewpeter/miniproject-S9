from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('displayuser/', views.displayuser, name='displayuser'),
    # path('displayuserfull/', views.displayuserfull, name='displayuserfull'),

 path('changeuserstatus/<str:email>/', views.changeuserstatus, name='changeuserstatus'),
    # You can add more paths for other views as needed
]