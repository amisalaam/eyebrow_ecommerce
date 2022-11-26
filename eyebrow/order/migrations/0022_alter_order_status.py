# Generated by Django 4.1.1 on 2022-11-24 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]
