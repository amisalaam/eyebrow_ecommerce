# Generated by Django 4.1.2 on 2022-12-04 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0042_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]
