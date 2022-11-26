from django.urls import path
from .import views

urlpatterns = [

    path('place-order/', views.placeorder, name = 'placeorder'),  
    path('proceed-to-pay/', views.razorpaycheck, name = 'razorpaycheck'),
    path('my-orders/', views.myorder, name = 'myorder'),
    path('view-order/<str:t_no>', views.vieworder, name = 'vieworder'),
    path('cancel_order/<str:t_no>', views.Cancel_order, name ='cancel_order'),

]