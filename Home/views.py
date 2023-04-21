from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .forms import UserAddForm 
from .decorators import Admin_Only
from .models import RecycleCloth,UserProfile
from django.contrib.auth.decorators import login_required
from AdminApp.models import Product,Videos

@Admin_Only
def Index(request):
    products = Product.objects.all()
    context = {
        "products":products
    }
    return render(request,"index.html",context)

@login_required(login_url='SignIn')
def AdminIndex(request):
    form = UserAddForm()
    user = User.objects.all()
    rrequests = RecycleCloth.objects.all().count()
    productc = Product.objects.all().count()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            group = Group.objects.get(name='merchant')
            new_user.groups.add(group) 
            
            messages.info(request,'Merchant Registered Successfully')
            return redirect('SignIn')
    context = {
        'form':form,
        "user":user,
        "rrequests":rrequests,
        "productc":productc
    }
    return render(request,'adminindex.html',context)

def MerchantIndex(request):
    videos = Videos.objects.all()
    context  = {
        "videos":videos
    }
    return render(request,"rcindex.html",context)



def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'User Registered Successfully')
            return redirect('SignIn')
    return render(request,"register.html",{"form":form})

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or password incorrect")
            return redirect('SignIn')
    return render(request,"login.html")

def SignOut(request):
    logout(request)
    return redirect('Index')

# user profile-------------------------------------------------------------
@login_required(login_url='SignIn')
def UserProfileView(request):
    userdata = None 
    if UserProfile.objects.filter(user  = request.user).exists():
        userdata = UserProfile.objects.get(user = request.user)
    if request.method == "POST":
        name = request.POST["name"]
        house = request.POST["house"]
        city = request.POST["city"]
        state = request.POST["state"]
        phone = request.POST["phone"]
        
        if UserProfile.objects.filter(user = request.user).exists():
            userpro = UserProfile.objects.get(user = request.user)
            userpro.name = name
            userpro.house = house 
            userpro.city = city 
            userpro.state = state
            userpro.phone = phone
            userpro.save()
            messages.info(request,"User Profile Updated") 
            return redirect('UserProfileView') 
        else:
            userpro = UserProfile.objects.create(name = name, house = house, city = city, state = state, phone = phone, points = 0,user = request.user)
            userpro.save()
            return redirect('UserProfileView')
    
    context = {
        "userdata":userdata
    }
    
    return render(request,'userprofile.html',context)


# recycle cloths --------------------------------------------------------------------------------
@login_required(login_url='SignIn')
def RecycleUserCloths(request):
    if not UserProfile.objects.filter(user  = request.user).exists():
        messages.info(request,"Plase Update User Profile to continue......") 
        return redirect('UserProfileView')
    data = None
    if RecycleCloth.objects.filter(user = request.user).exists():
        data = RecycleCloth.objects.filter(user = request.user)
    if request.method == "POST":
        cat = request.POST['cat']
        num = request.POST['number']
        weight = request.POST['weight']
        rcloth = RecycleCloth.objects.create(clothcategory = cat,clothweight = weight,numberofcloth = num,user = request.user,ponits = 0,status = "Submited for approvel")
        rcloth.save()
        messages.info(request,"Cloth Added for approvel")
        return redirect('RecycleUserCloths')
    
    context = {
        "data":data
    }
    
    return render(request,'clothrecycle.html',context)



