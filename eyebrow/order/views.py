from django.shortcuts import render,redirect
from .models import Order,OrderItem
from carts.models import Cart,CartItem
import random
from store.models import Product
from django.contrib import messages
from my_admin.models import Account
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


# Create your views here


@never_cache
@login_required(login_url=('signin')) 
def placeorder(request):
    if request.method =='POST':

        #cart check
        cart_items   = CartItem.objects.filter(user=request.user.id)
        if not cart_items:
            return redirect('store')

        currentuser = Account.object.filter(id=request.user.id).first()
        if not currentuser.first_name : # type: ignore
            currentuser.first_name = request.POST.get('first_name')# type: ignore
            currentuser.last_name = request.POST.get('last_name')# type: ignore
            currentuser.save()# type: ignore
            print(currentuser.first_name)# type: ignore


        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state= request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()   
             

        newOrder =Order()
        newOrder.user=request.user
        newOrder.first_name = request.POST.get('first_name')
        newOrder.last_name = request.POST.get('last_name')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state= request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')
        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')
        
        #taking total price
        cart_items   = CartItem.objects.filter(user=request.user)
        total = 0
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)

        newOrder.total_price = total 
        trackNo = 'eyebrow'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackNo) is None:
            trackNo = 'eyebrow'+str(random.randint(1111111,9999999))
        newOrder.tracking_no=trackNo
        newOrder.save()

        newOrderItems = CartItem.objects.filter(user=request.user)
        for item in newOrderItems:
            OrderItem.objects.create(
                order = newOrder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=request.user
            )
            #TO DECRESE THE QUANTITY OF PRODUCT
            orderproduct = Product.objects.filter(id=item.product_id).first() # type: ignore
            orderproduct.stock -=  item.quantity # type: ignore
            orderproduct.save() # type: ignore
            
        # TO CLEAR THE USER'S CART
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request,'Order Placed Successfully')
        
    payMode =  request.POST.get('payment_mode')
    if (payMode == "Paid by Razorpay" ):
       
        return JsonResponse ({'status':"Your order has been placed successfully"})
    elif (payMode == "COD" ):
        return redirect('myorder')
    return redirect('checkout') 

@never_cache
@login_required(login_url=('signin'))  # type: ignore
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)  
    total_price = 0 
    if cart:
            
        for item in cart:
            total_price   += (item.product.price * item.quantity)

        return JsonResponse({
            'total_price' : total_price

        })
    else:
        return redirect('store')


#MY ORDER FUNCTION
@never_cache
@login_required(login_url=('signin')) 
def myorder(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    context ={
        'orders':orders
    }
    return render(request,'order/myorder.html',context)


@never_cache
@login_required(login_url=('signin')) 
def vieworder(request,t_no):
    order =Order.objects.filter(tracking_no=t_no,user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
        
    }
    return render(request,'order/vieworder.html',context)


def Cancel_order(request,t_no):
    order =Order.objects.get(tracking_no=t_no,user=request.user)
    order.status ='Cancelled'
    order.save()
    return redirect('myorder')

   

  
      








        

    
         

