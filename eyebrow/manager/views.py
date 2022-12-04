from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.views.decorators.cache import never_cache
from my_admin.models import Account
from django.db.models import Q
from django.core.paginator import Paginator
from store.models import Product
from .form import ProductForm,VariationForm,BannerForm,BrandAdForm,MultipleImagesForm
from order.models import Order,OrderItem
from store.models import Variation,category,ReviewRating,MultipleImages
from users.models import Banner,BrandAd


# ADMIN DASHBOARD
@never_cache
@login_required(login_url='signin')
def manager_dashboard(request,):
    if request.user.is_superadmin:
        user_count = Account.object.filter(is_superadmin=False).count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.filter().count()
        category_count = category.objects.all().count()

        context = {
            'user_count': user_count,
            'product_count': product_count,
            'order_count' : order_count,
            'category_count' : category_count,
        }

        return render(request,'manager/manager_dashboard.html',context)
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
  if request.user.is_superadmin: 
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
  else:
    return redirect('home')  
  
#ADD PRODUCT
@never_cache
@login_required(login_url='signin')  # type: ignore
def add_product(request):
  if request.user.is_superadmin:
    if request.method == 'POST':
      form = ProductForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
          return redirect('product_management')
      else:
       messages.error(request,'Invalid form')
       return redirect('add_product')     
    else:
      form = ProductForm()
      context = {
          'form': form
       }
      return render(request, 'manager/add_product.html', context)
  else:
    return redirect('home')    


#EDIT PRODUCT
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)
    if request.user.is_superadmin:
      if request.method == 'POST':
          try:
              form = ProductForm(request.POST, request.FILES, instance=product)
              if form.is_valid():
                  form.save()
                  messages.success(request,'Product edited succefully')
                  return redirect('product_management')
              else:
                messages.error(request,'Invalid form') 
                return redirect('edit_product')     

          except Exception as e:
              raise e

      context = {
          'product': product,
          'form': form
      }
      return render(request, 'manager/edit_product.html', context) 
    else:
      return redirect('home')  

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
  if request.user.is_superadmin:
    if request.method == 'POST':
        key = request.POST['key']
        order = Order.objects.filter( Q(tracking_no_startswith=key) | Q(useremailstartswith=key) | Q(first_name_startswith=key)).order_by('-id')
    else:
        order = Order.objects.all().order_by('-id') 
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)

    context = {
        'order': paged_order
        }
    return render(request, 'manager/order_management.html',context)
  else:
    return redirect('home')  

#VIEW MANAGEMENT ORDER
def manager_vieworder(request,tracking_no):
  if request.user.is_superadmin:
    order = Order.objects.filter(tracking_no=tracking_no,user=request.user.id).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'manager/manager_vieworder.html',context)
  else:
    return redirect('home') 

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
    return redirect('order_management')

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
  if request.user.is_superadmin:
    categories = category.objects.all().order_by('id')

    context = {
          'categories': categories
      }
    return render(request, 'manager/category_management.html', context)
  else:
    return redirect('home')  

#ADD CATEGORY
def add_category(request):
  if request.user.is_superadmin:
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
  else:
    return redirect('home')  

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

    paginator = Paginator(variations, 15)
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
         messages.error(request,'Invalid form')
         return redirect('add_variation')    

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
          messages.error(request,'Invalid form') 
          return redirect('update_variation')     
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





# REVIEW MANAGMENT
@never_cache
@login_required(login_url='signin')
def review_management(request):
  reviews = ReviewRating.objects.all()
  context = {
    'reviews': reviews
  }
  return render(request, 'manager/review_management.html', context)

#BLOCK REVIEW
@never_cache
@login_required(login_url='signin')
def review_block(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status = False
  review.save()
  return redirect('review_management')

# UNBLOCK REVIEW
@never_cache
@login_required(login_url='signin')
def review_unblock(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status= True
  review.save()
  return redirect('review_management') 




# BANNER MANAGEMENT
@never_cache
@login_required(login_url='signin')
def banner_management(request):
  banners = Banner.objects.all().order_by('id')
  context = {
    'banners': banners
  }
  return render(request, 'manager/banner_management.html', context)

#ADD BANNER
@never_cache
@login_required(login_url='signin')
def add_banner(request):
  if request.method == 'POST':
    form = BannerForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('banner_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('add_banner') 

  else:
    form = BannerForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_banner.html', context)

# UPDATE BANNER
@never_cache
@login_required(login_url='signin')
def update_banner(request, banner_id):
  banner =  Banner.objects.get(id = banner_id)
  form = BannerForm(instance = banner)
  if request.method == 'POST':
    form = BannerForm(request.POST, request.FILES, instance = banner)
    if form.is_valid():
      form.save()
      messages.success(request,'Added Succefully')
      return redirect('banner_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('update_banner')   
  context = {
    'form':form
  }
  return render(request, 'manager/add_banner.html', context) 

#DELETE BANNER
@never_cache
@login_required(login_url='signin')
def delete_banner(request, banner_id):
  banner = Banner.objects.get(id = banner_id)
  banner.delete()
  messages.success(request,'Item deleted successfully')
  return redirect('banner_management')



#MULTIPLE IMAGES MANAGEMENT
@never_cache
@login_required(login_url='signin')
def multiple_image_management(request):
  multipleimages = MultipleImages.objects.all().order_by('id')
  paginator = Paginator(multipleimages, 10)
  page = request.GET.get('page')
  multipleimages = paginator.get_page(page)

  context = {
    'multipleimages': multipleimages
  }
  return render(request, 'manager/multiple_image_management.html', context)
  
#ADD MULTIPLE IMAGES
@never_cache
@login_required(login_url='signin')
def add_multiple_images(request):  # type: ignore
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.error(request,'')
      return redirect('add_multiple_images')
    else:
      print(form.errors)
      messages.error(request,'Invalid form') 
      return redirect('add_multiple_images') 
  else:
    form = MultipleImagesForm()

  context = {
    'form': form
  }
  return render(request,'manager/add_multiple_images.html',context)

# UPDATE MULTIPLE IMAGE
@never_cache
@login_required(login_url='signin')
def update_multiple_images(request,multi_id):
  multipleimages = MultipleImages.objects.get(id=multi_id)
  form = MultipleImagesForm(instance = multipleimages)
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES, instance = multipleimages)
    if form.is_valid():
      form.save()
      messages.success(request,'Added Succefully')
      return redirect('multiple_image_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('update_multiple_images')   
  context = {
    'form':form
  }
  return render(request, 'manager/update_multiple_images.html', context)


# DELETE MULTIPLEIMAGES
@never_cache
@login_required(login_url='signin')
def delete_multiple_images(request, multi_id):
  multipleimages = MultipleImages.objects.get(id = multi_id)
  multipleimages.delete()
  return redirect('multiple_image_management')




# BRANDADS MANAGEMENT
@never_cache
@login_required(login_url='signin')
def brandads_management(request):
  brandads = BrandAd.objects.all().order_by('id')
  context = {
    'brandads': brandads,
  }
  return render(request, 'manager/brandads_management.html', context)

#ADD BRAND ADS
@never_cache
@login_required(login_url='signin')
def add_brandads(request):
  if request.method == 'POST':
    form = BrandAdForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('brandads_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('add_brandads') 

  else:
    form = BrandAdForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_brandads.html', context)

# UPDATE BRAND ADS
@never_cache
@login_required(login_url='signin')
def update_brandads(request, brandads_id):
  brandads =  BrandAd.objects.get(id = brandads_id)
  form = BrandAdForm(instance = brandads)
  if request.method == 'POST':
    form = BrandAdForm(request.POST, request.FILES, instance = brandads)
    if form.is_valid():
      form.save()
      return redirect('brandads_management')
    else:
      messages.error(request,'Invalid form')  
  context = {
    'form':form
  }
  return render(request, 'manager/add_brandads.html', context) 

#DELETE BRAND ADS
@never_cache
@login_required(login_url='signin')
def delete_brandads(request, brandads_id):
  brandads = BrandAd.objects.get(id = brandads_id)
  brandads.delete()
  return redirect('brandads_management')





  



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





