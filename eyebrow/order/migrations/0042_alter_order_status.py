# Generated by Django 4.1.2 on 2022-11-30 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0041_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]
