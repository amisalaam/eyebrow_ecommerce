from django.db import models
from my_admin.models import Account

# Create your models here.





#  New user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField( upload_to='userprofile',null=True)
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.first_name


    def full_address(self):
        return f'{ self.address_line_1 } { self.address_line_2 }'

class Banner(models.Model):
    img = models.ImageField(upload_to='photos/baners', blank=False)
    alt_text = models.CharField(max_length=300,blank=False)
    caption = models.CharField(max_length=50,blank=False)
    brandslogan = models.CharField(max_length=100,blank=False)
    Brandname=models.CharField(max_length=100,blank=False)



class BrandaAd(models.Model):
    img = models.ImageField(upload_to='photos/brandad', blank=False)
    alt_text = models.CharField(max_length=300,blank=False)
    caption = models.CharField(max_length=50,blank=False)
    Brandname=models.CharField(max_length=100,blank=False)




