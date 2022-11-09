

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('myaccount/', views.myaccount, name = 'myaccount'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('change_password/', views.change_password, name = 'change_password'),


]
