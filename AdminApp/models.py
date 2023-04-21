from django.db import models
from django.contrib.auth.models import User 

options = (("Mens","Mens"),("Womens","Womens"),("Kids","Kids"),("Other","Other"))

class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=25,choices=options)
    price = models.FloatField()
    point = models.IntegerField()
    image = models.FileField(upload_to="product_image")
    stock = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)


class CartItems(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.FloatField(null=True,blank=True)
    
class CheckOuts(models.Model):
    
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    py_status = models.BooleanField(default=False)
    
class Videos(models.Model):
    name = models.CharField(max_length=20)
    video = models.FileField(upload_to="videos")
    