# Generated by Django 3.2.14 on 2023-04-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_recyclecloth_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recyclecloth',
            name='recycled_product',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
