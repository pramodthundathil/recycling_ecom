# Generated by Django 3.2.14 on 2023-04-21 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0002_cartitems_checkouts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('video', models.FileField(upload_to='videos')),
            ],
        ),
    ]
