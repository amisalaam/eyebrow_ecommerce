# Generated by Django 4.1.2 on 2022-11-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='brandslogan',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='caption',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
