from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),

    # ACTIVATION URLS

    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

     # RESET PASSWORD EMAIL URLS

    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),

     # RESET PASSWORD URLS
    path('resetpassword/',views.resetpassword,name='resetpassword'),
]
