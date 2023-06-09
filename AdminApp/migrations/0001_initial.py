# Generated by Django 3.2.14 on 2023-04-21 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('category', models.CharField(choices=[('Mens', 'Mens'), ('Womens', 'Womens'), ('Kids', 'Kids'), ('Other', 'Other')], max_length=25)),
                ('price', models.FloatField()),
                ('point', models.IntegerField()),
                ('image', models.FileField(upload_to='product_image')),
                ('stock', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
