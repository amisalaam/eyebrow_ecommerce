# Generated by Django 4.1.10 on 2023-09-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=70)),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=70)),
                ('password', models.CharField(max_length=70)),
                ('Confirm_password', models.CharField(max_length=70)),
                ('phone_number', models.CharField(max_length=70)),
            ],
        ),
    ]
