# Generated by Django 4.1.1 on 2022-11-24 03:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0009_alter_reviewrating_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReviewRating',
            new_name='ReviewRatings',
        ),
    ]
