
from category.models import category
from django.shortcuts import render,get_object_or_404
from store.models import Product,MultipleImages
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q


 
# Create your views here.
def store (request,category_slug=None ):
    categories=None
    products = None
    if category_slug != None:
        categories =get_object_or_404(category,slug=category_slug)
        products= Product.objects.filter(category=categories,is_available =True).order_by('id')
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count =products.count()
    else:
        products = Product.objects.all().filter(is_available = True)
        paginator=Paginator(products,12)
        page =request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count= products.count()


    context =  {
        'products': paged_products, 
        'products_count':products_count,
    }
    return render(request, 'store/store1.html', context) 



#Product Details and multiple images
def product_detail(request, category_slug,product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        multiple_images = MultipleImages.objects.filter(product=single_product)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product' : single_product,
        'in_cart'        : in_cart,
        'multiple_images': multiple_images,
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
    
    return render(request, 'store/store1.html',context) 
  


