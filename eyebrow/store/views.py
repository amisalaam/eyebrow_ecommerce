
from category.models import category
from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product,MultipleImages
from carts.models import CartItem,WishlistItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from . models import ReviewRating
from . form import ReviewForm
from django.contrib import messages
from order.models import OrderItem



 
# Create your views here.
def store (request,category_slug=None ):
    categories=None
    products = None
    if category_slug != None:
        categories =get_object_or_404(category,slug=category_slug)
        products= Product.objects.filter(category=categories,is_available =True).order_by('-created_date')
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count =products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('-created_date')
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count= products.count()


    context =  {
        'products': paged_products, 
        'products_count':products_count,
    }
    return render(request, 'store/store.html', context) 



#Product Details and multiple images
def product_detail(request, category_slug,product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        multiple_images = MultipleImages.objects.filter(product=single_product)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    try:
        orderitem=None
        if request.user.is_authenticated:
         orderitem =  OrderItem.objects.filter(user=request.user,product_id=single_product.id).exists()  # type: ignore
    except OrderItem.DoesNotExist:
        orderitem = None 

    #showing the old reviews
    reviwes= ReviewRating.objects.filter(product_id=single_product.id,status=True)  # type: ignore
    wishlist=None
    if request.user.is_authenticated:
        wishlist= WishlistItem.objects.filter(product=single_product)
    

    context = {
        'single_product' : single_product,
        'in_cart'        : in_cart,
        'multiple_images': multiple_images,
        'orderitem'      : orderitem,
        'reviwes'        : reviwes,
        'wishlist'       : wishlist
        }           
    return render (request,'store/product_detail.html',context)



#Search function
def search(request,products=0,products_count=0):
    if 'keyword' in request.GET:
        keyword =request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword ))
            products_count= products.count()
        else:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword ))
            products_count= products.count()         
    
    context={
        'products':products,
        'products_count':products_count,

    }
    
    return render(request, 'store/store.html',context) 
  


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:

            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating() 
                data.subject = form.cleaned_data['subject']  # type: ignore
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id   # type: ignore
                data.user_id = request.user.id    # type: ignore
                data.save()
    

                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
