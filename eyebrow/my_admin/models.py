
from distutils.command.upload import upload
from hashlib import blake2b
import profile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class myaccountmanager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number,password=None) :
        if not email:
            raise ValueError('User must have an email ')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name= last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, first_name, last_name, username,phone_number, password, email):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=70, unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=70, unique=True)
    phone_number = models.CharField(max_length=70, unique=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']
    object = myaccountmanager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

#New user profile model

# class UserProfile(models.Model):
#  user = models.OneToOneField(Account,on_delete=models.CASCADE)
#  address_line_1=models.CharField(blank= True, max_length=100)
#  address_line_2=models.CharField(blank= True, max_length=100)
#  profile_picture = models.ImageField(blank=True,upload_to='userprofile')
#  city = models.CharField(blank=True,max_length=50)
#  state = models.CharField(blank=True,max_length=50)
#  country=models.CharField(blank=True,max_length=50)


#  def __str__(self):
#     return self.user.first_name

# def full_address(self):
#     return f'{self.address_line_1 } {self.address_line_2 }'

