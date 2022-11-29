from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.views.decorators.cache import never_cache
from my_admin.models import Account
from django.db.models import Q
from django.core.paginator import Paginator
from store.models import Product
from .form import ProductForm,VariationForm
from order.models import Order,OrderItem
from store.models import Variation,category


# ADMIN DASHBOARD
@never_cache
@login_required(login_url='signin')
def manager_dashboard(request,):
    if request.user.is_superadmin:
        return render(request,'manager/manager_dashboard.html')
    else:
        return redirect('home')



#USER MANAGMENT 
@never_cache
@login_required(login_url='signin')
def user_management(request):
    if request.user.is_superadmin:
        if request.method == "POST":
            key = request.POST['key']
            users = Account.object.filter( Q(first_name__startswith=key) | Q(last_name__startswith=key) | Q(username__startswith=key) | Q(email__startswith=key),is_superadmin=False).order_by('id')
        else:
            users = Account.object.filter(is_superadmin=False).order_by('id')

        paginator = Paginator(users,10)
        page = request.GET.get('page')
        paged_users = paginator.get_page(page)
        context = {
        'users' : paged_users
        }
        return render(request, 'manager/user_management.html',context)
    else:
        return redirect('signin')    

# BLOCK USER
@never_cache
@login_required(login_url='signin')
def block_user(request,user_id):
    user = Account.object.get(id =user_id)
    user.is_active = False
    user.save()
    return redirect ('user_management') 

# USER UNBLOCK
@never_cache
@login_required(login_url='signin')
def unblock_user(request,user_id):
    user = Account.object.get(id =user_id)
    user.is_active = True
    user.save()
    return redirect ('user_management') 



#PRODUCT  MANAGEMENT
@never_cache
@login_required(login_url='signin')
def product_management(request):
  if request.method == "POST":
    key = request.POST['key']
    products = Product.objects.filter(Q(product_name__icontains=key) | Q(slug__startswith=key) | Q(category__category_name__startswith=key)).order_by('id')
  else:
    products = Product.objects.all().order_by('id')

  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)
  
  context = {
    'products': paged_products
  }
  return render(request, 'manager/product_management.html', context)
  
#ADD PRODUCT
@never_cache
@login_required(login_url='signin')  # type: ignore
def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('product_management')
  else:
    form = ProductForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_product.html', context)

#EDIT PRODUCT
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        try:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request,'Product edited succefully')

                return redirect('product_management')

        except Exception as e:
            raise e

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'manager/edit_product.html', context) 

# DELETE PRODUCTS
@never_cache
@login_required(login_url='signin')
def delete_product(request, product_id):
  product = Product.objects.get(id=product_id)
  product.delete()
  messages.error(request,'Product deleted Successfully')
  return redirect('product_management')




#ORDER MANAGEMENT
def order_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        order = Order.objects.filter( Q(tracking_no_startswith=key) | Q(useremailstartswith=key) | Q(first_name_startswith=key)).order_by('id')
    else:
        order = Order.objects.filter(user=request.user).order_by('id') 
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)

    context = {
        'order': paged_order
        }
    return render(request, 'manager/order_management.html',context)

#VIEW MANAGEMENT ORDER
def manager_vieworder(request,tracking_no):
    order = Order.objects.filter(tracking_no=tracking_no,user=request.user.id).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'manager/manager_vieworder.html',context)

#ACCEPT ORDER
def manager_accept_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Out For Shipping'
    order.save()
    return redirect('order_management')  

#SHIP ORDER    
def manager_ship_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Shipped'
    order.save()
    return redirect('manager_vieworder')

#DELIVERED ORDER
def manager_delivered_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Delivered'
    order.save()
    return redirect('order_management')          

#CANCEL ORDER
def manager_cancel_order(request,tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_management')


#CATOGERY MANAGEMENT
def category_management(request):
  categories = category.objects.all().order_by('id')

  context = {
        'categories': categories
    }
  return render(request, 'manager/category_management.html', context)

#ADD CATEGORY
def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']

            categories = category(
                category_name=category_name,
                description=category_description
            )

            categories.save()
            return redirect('category_management')
        except Exception as e:
            raise e

    return render(request, 'manager/add_category.html')

#UPDATE CATEGORY  
def update_category(request, category_id):
    try:
        categories = category.objects.get(id=category_id)

        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_description = request.POST['category_description']
            categories.category_name = category_name
            categories.description = category_description

            categories.save()
            return redirect('category_management')

        context = {
            'category': categories,
        }
    except Exception as e:
        raise e

    return render(request, 'manager/update_category.html', context)

#DELETE CATEGORY
def delete_category(request, category_id):
    categories = category.objects.get(id=category_id)
    print(categories)
    categories.delete()
    return redirect('category_management')



# VARIATION MANAGEMENT
def variation_management(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        variations = Variation.objects.filter(Q(product_product_name__icontains=keyword) | Q(
            variation_category__icontains=keyword) | Q(variation_value__icontains=keyword)).order_by('id')

    else:
        variations = Variation.objects.all().order_by('id')

    paginator = Paginator(variations, 10)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations': paged_variations
    }
    return render(request, 'manager/variation_management.html', context)

# ADD VARIATION
def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm()

    context = {
        'form': form
    }
    return render(request, 'manager/add_variation.html', context)

#UPDATE VARIATION
def update_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_management')
    else:
        form = VariationForm(instance=variation)
    context = {
        'variation': variation,
        'form': form
    }
    return render(request, 'manager/update_variation.html', context)

#DELETE VARIATION
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    variation.delete()
    return redirect('variation_management')    


# CHANGE ADMINS PASSWORD
@never_cache
@login_required(login_url='signin')
def admin_change_password(request):
  if request.method == 'POST':
    current_user = request.user
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    
    if new_password == confirm_password:
      if check_password(current_password, current_user.password):
        if check_password(new_password, current_user.password):
          messages.warning(request, 'Current password and new password is same')
        else:
          hashed_password = make_password(new_password)
          current_user.password = hashed_password
          current_user.save()
          messages.success(request, 'Password changed successfully')
      else:
        messages.error(request, 'Wrong password')
    else:
      messages.error(request, 'Passwords does not match')
  
  return render(request, 'manager/admin_change_password.html')





