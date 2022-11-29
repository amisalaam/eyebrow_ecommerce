
from django.urls import reverse
from django.db import models
from category.models import category
from my_admin.models import Account
from django.db.models import Avg ,Count
from autoslug import AutoSlugField

# Create your models here.



#product model
class Product(models.Model):
    product_name =models.CharField(max_length=200,unique=True)
    slug         =AutoSlugField(max_length=200,unique=True)
    description  =models.TextField(max_length=1000)
    price        = models.IntegerField ()
    images       = models.ImageField(upload_to='photos/products')
    is_available =models.BooleanField(default=True)
    stock        = models.IntegerField()
    category     =models.ForeignKey(category,on_delete=models.CASCADE)
    created_date =models.DateTimeField(auto_now_add = True)
    modified_date=models.DateTimeField(auto_now =True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug]) 

    def __str__(self):
        return self.product_name

    def averageReview(self):    
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:  # type: ignore
            avg = float(reviews['average'])  # type: ignore
        return avg  

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
         




#Variation Model 
variation_category_choise=(
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product            =models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category =models.CharField(max_length=100,choices=variation_category_choise)
    variation_value    =models.CharField(max_length=100)
    is_active          =models.BooleanField(default=True)
    created_date       =models.DateTimeField(auto_now_add = True)

    objects = VariationManager()
         

    def __str__(self):
        return self. variation_value 


#multiple images
class MultipleImages(models.Model):
    image = models.ImageField(upload_to='media/product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(max_length=20)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.subject
