from django.db import models

# Create your models here.

class RegForm(models.Model):
    username = models.CharField(max_length = 70)
    first_name = models.CharField(max_length = 70)
    last_name = models.CharField(max_length = 70)
    email = models.EmailField(max_length = 70)
    password = models.CharField(max_length = 70)
    Confirm_password = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length = 70)

