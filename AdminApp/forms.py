from django.forms import ModelForm
from .models import Product,Videos

class ProductAddForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name",'category','point','price','image','stock']
        
class VideosAddForm(ModelForm):
    class Meta:
        model = Videos
        fields = "__all__"