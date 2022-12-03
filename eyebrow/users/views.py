
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from  store.models import Product
from .models import *
# from orders.model import order
from .forms import UserForm, UserProfileForm
from django.core.paginator import Paginator




# Create your views here.


def home(request):
    products = Product.objects.filter(is_available = True).order_by('-created_date')[0:12]
    banners = Banner.objects.all().order_by('-id')[0:3]
    brandad= BrandAd.objects.all().order_by('-id')[0:3]
    paginator=Paginator(products,12)
    context =  {
        'products':products,
        'paginator':paginator,
        'banners': banners,
        'brandad' : brandad
    }

    return render(request,'users/home1.html',context)


# MYACCOUNT CONDITION (DASH BOARD)
@login_required(login_url='signin')
def myaccount(request):
    # order=order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    # orders_count=order.count()
    
    userprofile = UserProfile.objects.filter(user_id=request.user.id)

    context = {
    #     'orders_count':orders_count,
    'userprofile':userprofile
    
     }


    return render(request, 'users/myaccount.html',context)
  


# EDIT PROFILE CONDITION
@login_required(login_url='signin')
def edit_profile(request):
    if UserProfile.objects.filter(user=request.user):
        userprofile = get_object_or_404(UserProfile, user=request.user)
    else: 
        userprofile = UserProfile.objects.create(user=request.user)   
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form'   : user_form,
        'profile_form': profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'users/edit_profile.html', context)



    # Change Password 

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password     = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.object.get(username__iexact =request.user.username)

        if new_password==confirm_password:
            success=user.check_password(current_password)
            if current_password==new_password:
             messages.error(request,'Current password and New password are same ')
             return redirect('change_password')
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Changed')
                return redirect('signin')

    return render (request,'users/change_password.html')