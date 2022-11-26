

from django.shortcuts import render, redirect
from my_admin.models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignup, UserSignin
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import _cart_id

#REDIRECTING USER TO THE CHECKOUT PAGE
import requests

#VERIFICATION IMPORTS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 


#SIGNUP
def register(request):
    if request.method=='POST':
        form=UserSignup(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            phone_number=form.cleaned_data['phone_number']
            # confirm_password=form.cleaned_data['confirm_password']
            user = Account.object.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password, phone_number=phone_number)
                
            user.save()
            
            # USER ACTIVATION
            current_site=get_current_site(request)
            mail_subject='ACTIVATION CODE FROM EYE BROW'
            message=render_to_string('authentication/account_verification_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': default_token_generator.make_token(user),
                                       })
            to_email=email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Check Your Email For Activation Link To Activate Your Account')
            return redirect('/authentication/signin/?command=verification&email='+email)
    else:
        form = UserSignup
    form = UserSignup()
    context = {
        'form': form,
    }
    return render(request, 'authentication/user_signup.html', context)


# SIGNIN CONDITIONS 
def signin(request ):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email         = request.POST['email']
            password      = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                try:
                 cart =Cart.objects.get(cart_id=_cart_id(request))
                 is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                 if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item: 
                        variation = item.variation.all()
                        product_variation.append(list(variation))
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)   # type: ignore
                    for product in product_variation:
                        if product in ex_var_list:
                            index = ex_var_list.index(product) 
                            item_id =id[index]
                            item =CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user =user   # type: ignore
                            item.save()
                        else:
                            cart_item =CartItem.objects.filter(cart=cart)       
                            for item in cart_item:
                                item.user = user      # type: ignore
                                item.save()
                except:
                      pass            
                auth.login(request, user)
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query    # type: ignore


                    #spliting the next in to  a dict
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('home')  
                
            else:
                messages.error(request, 'Incorrect username or password')
                return redirect('signin')
        form = UserSignin()
        return render(request, 'authentication/user_signin.html', {'form': form})




#  LOGOUT CONDITION 
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('signin')



#EMAIL_ACTIVARTION CONDITION
def activate (request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations Your account is activated ')
        return redirect('signin')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register') 
         

#FORGOT PASSWORD CONDITIONS
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.object.filter(email=email).exists():
            user=Account.object.get(email__iexact=email)

            #RESET PASSWORD EMAIL SENDING CONDITION 
            current_site = get_current_site(request)
            mail_subject = 'RESET YOUR PASSWORD '
            message = render_to_string('authentication/reset_password_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': default_token_generator.make_token(user),
                                       })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email')
            return redirect('forgotpassword')
        else:
         messages.error(request,'Account does not exist')  
         return redirect('forgotpassword')  
    form = UserSignup()
    return render(request,'authentication/forgotpassword.html', {'form' : form})



 #PASSWORD RESET EMAIL CONDITION  URLS
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid # type: ignore
        messages.success(request,'Please reset Your password ')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired ')  
        return redirect('signin')      



#RESET PASSWORD CONDITION
def resetpassword(request):
    if request.method    =='POST':
        password         = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid     = request.session.get('uid')
            user    = Account.object.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfully')
            return redirect ('signin')
        else:
         messages.error(request,'Password does not match')
         return redirect('resetpassword')
    return render(request,'authentication/resetpassword.html')
    
    
