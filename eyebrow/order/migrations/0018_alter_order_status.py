# Generated by Django 4.1.1 on 2022-11-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
    ]
