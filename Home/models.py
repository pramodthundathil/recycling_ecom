from django.db import models
from django.contrib.auth.models import User 

class RecycleCloth(models.Model):
    clothcategory = models.CharField(max_length=255)
    clothweight = models.FloatField()
    numberofcloth = models.IntegerField()
    ponits = models.IntegerField(null=True,blank=True)
    approvel = models.BooleanField(default=False)
    rejection = models.BooleanField(default=False)
    status = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recycled_product = models.CharField(max_length=255,null=True,blank=True)
    
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    house = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    points = models.IntegerField(null=True)

