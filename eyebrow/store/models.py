
from django.urls import reverse
from django.db import models
from category.models import category

# Create your models here.



#product model
class Product(models.Model):
    product_name =models.CharField(max_length=200,unique=True)
    slug         =models.SlugField(max_length=200,unique=True)
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
         

    def __unicode__(self):
        return self.product
