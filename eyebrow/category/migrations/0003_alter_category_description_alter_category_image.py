# Generated by Django 4.1.1 on 2022-10-31 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='photos/categories'),
        ),
    ]