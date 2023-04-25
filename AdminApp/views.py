from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from Home.models import UserProfile, RecycleCloth
from .forms import ProductAddForm,VideosAddForm
from .models import Product,CartItems,CheckOuts,Videos
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest

# Create your views here.

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def RecycleRequests(request):
    recloth = RecycleCloth.objects.all()
    context = {
        "recloth":recloth
    }
    return render(request,"recyclerequest.html",context)

def ApproveReq(request,pk):
    rcloth = RecycleCloth.objects.get(id = pk)
    rcloth.approvel = True
    rcloth.status = "Approved"
    rcloth.rejection = True
    rcloth.save()
    messages.info(request,"Item Updated")
    return redirect('RecycleRequests')

def RejectReq(request,pk):
    rcloth = RecycleCloth.objects.get(id = pk)
    rcloth.approvel = False
    rcloth.status = "Rejected"
    rcloth.rejection = False
    rcloth.save()
    messages.info(request,"Item Updated")
    return redirect('RecycleRequests')

def CollectReq(request,pk):
    rcloth = RecycleCloth.objects.get(id = pk)
    rcloth.approvel = True
    rcloth.rejection = True
    rcloth.status = "Cloth Collected"
    rcloth.ponits = rcloth.clothweight * 10 
    rcloth.save()
    userpro = UserProfile.objects.get(user = rcloth.user)
    userpro.points = userpro.points + rcloth.ponits
    userpro.save()
    messages.info(request,"Item Updated")
    return redirect('RecycleRequests')


def SentForRecycleReq(request,pk):
    rcloth = RecycleCloth.objects.get(id = pk)
    rcloth.approvel = True
    rcloth.status = "Cloth Sent For Recycle"
    rcloth.rejection = True
    rcloth.save()
    messages.info(request,"Item Updated")
    return redirect('RecycleRequests')
    
def RecycledReq(request,pk):
    rcloth = RecycleCloth.objects.get(id = pk)
    rcloth.approvel = True
    rcloth.status = "Cloth Recycled"
    rcloth.rejection = True
    rcloth.save()
    messages.info(request,"Item Updated")
    return redirect('RecycleRequests')

def ProductAdmin(request):
    product = Product.objects.filter(user = request.user)
    form = ProductAddForm()
    if request.method == "POST":
        form = ProductAddForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.save()
            data.user = request.user
            data.save()
            messages.info(request,"Product Added To List")
            return redirect('ProductAdmin')
    
    context = {
        "form":form,
        "product":product
    }
    return render(request,"productsadmin.html",context)



# cart -----------------

@login_required(login_url="SignIn")
def AddTocart(request,pk):
    product = Product.objects.get(id = pk)
    if CartItems.objects.filter(product = product,user = request.user).exists():
        cart = CartItems.objects.get(product = product,user = request.user)
        cart.quantity = cart.quantity + 1
        cart.price = cart.price + cart.price
        cart.save()
    else:
        cart = CartItems.objects.create(product = product,quantity = 1,user = request.user,price = product.price)
        cart.save()
    return redirect("Cart")

@login_required(login_url="SignIn")
def Cart(request):
    cartitems = CartItems.objects.filter(user = request.user)
    price = 0
    points = 0
    for item in cartitems:
        price = price + item.price
        points = points + item.product.point
        
    context = {
        'cart':cartitems,
        'cartlen':len(cartitems),
        'price':price,
        "points":points
    }
    return render(request,"cart.html",context)

@login_required(login_url="SignIn")
def CheckOut(request):
    cart = CartItems.objects.filter(user = request.user)
    total = 0
    for items in cart:
        ckout = CheckOuts.objects.create(Product = items.product,quantity = items.quantity,price = items.price,user = request.user, status = "Item Ordered")
        ckout.save()
        total = total + float(items.price)
        items.delete()
    
    context = {
        
        "total":total
    }
    currency = 'INR'
    amount = total * 100 # Rs. 200
    

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'paymenthandlercus'

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = ckout.id,
    # context['amt'] = (product1.Product_price)*float(qty)
       
    return render(request,"Makepayment.html",context)

@csrf_exempt
def paymenthandlercus(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
@login_required(login_url="SignIn")
def IncreaseCartQunty(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.quantity = cart.quantity + 1
    cart.price = cart.price + cart.product.price 
    cart.save()
    return redirect('Cart')

@login_required(login_url="SignIn")
def DecreaseCartQunty(request,pk):
    cart = CartItems.objects.get(id = pk)
    if cart.quantity == 1:
        cart.delete()
    else:
        cart.quantity = cart.quantity - 1
        cart.price = cart.price - cart.product.price 
        cart.save()
    return redirect('Cart')

@login_required(login_url="SignIn")
def DeleteCart(request,pk):
    CartItems.objects.get(id = pk).delete()
    return redirect('Cart')

@login_required(login_url="SignIn")
def Myorders(request):
    order = CheckOuts.objects.filter(user = request.user)
    context = {
        'order':order
    }
    return render(request,"myorders.html",context)

@login_required(login_url="SignIn")
def deleteorderedhistory(request,pk):
    CheckOuts.objects.get(id = pk).delete()
    messages.info(request,"Product Deleted")
    return redirect("Myorders")

@login_required(login_url="SignIn")
def Customerorders(request):
    order = CheckOuts.objects.all()
    context = {
        "order":order
    }
    return render(request,"customerorder.html",context)

@login_required(login_url="SignIn")
def ChangeToDespached(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Despached"
    order.save()
    return redirect("Customerorders")

@login_required(login_url="SignIn")
def ChangeToDelivered(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Delivered"
    order.save()
    return redirect("Customerorders")

@login_required(login_url="SignIn")
def ChangeToCanceled(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Order Cancelled By Merchant"
    order.save()
    return redirect("Customerorders")

@login_required(login_url="SignIn")
def DelateOrderMerchant(request,pk):
    CheckOuts.objects.get(id = pk)
    messages.info(request,"Order Deleted")
    return redirect("Customerorders")

def ViewAddress(request,pk):
    ckout = CheckOuts.objects.get(id = pk)
    prodata = UserProfile.objects.get(user = ckout.user)
    context = {
        "prodata":prodata
    }
    return render(request,'customeraddress.html',context)


def Checkoutwithpoints(request):
    cartitems = CartItems.objects.filter(user = request.user)
    if UserProfile.objects.filter(user = request.user).exists():
        UserPro = UserProfile.objects.get(user = request.user)
        points = 0
        for item in cartitems:
            points = points + item.product.point
        if points > UserPro.points:
            messages.info(request,"You Dont Have Points To Purchase The item")
            return redirect("Cart")
        else:
            cart = CartItems.objects.filter(user = request.user)
            total = 0
            for items in cart:
                ckout = CheckOuts.objects.create(Product = items.product,quantity = items.quantity,price = items.price,user = request.user, status = "Item Ordered")
                ckout.save()
                total = total + float(items.price)
                items.delete()
                UserPro.points = UserPro.points - points
                UserPro.save()
                return render(request,"Paymentconfirm.html")
    else:
        messages.info(request,"Please Upadate User Profile")
        return redirect('Cart')
        
        
def UplaodTutorialVideos(request):
    form = VideosAddForm()
    videoi = Videos.objects.all()
    if request.method == "POST":
        form = VideosAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"Video Saved")
            return redirect('UplaodTutorialVideos')
    context = {
        "form":form,
        "videoi":videoi
    }
    return render(request,"uploadvideo.html",context)

def SearchByName(request):
    if request.method == "POST":
        district = request.POST["val"]
        product = Product.objects.filter(name__contains = district)
        return render(request, "search.html",{"search":district,"product":product})
    
def ClothForRecycle(request):
    rcitems = RecycleCloth.objects.filter(approvel = True)
    context = {
        "rcitems":rcitems
    }
    return render(request,"recyclepoduct.html",context)

def UpdateReStatus(request,pk):
    item = RecycleCloth.objects.get(id = pk)
    if request.method == "POST":
        rtype = request.POST["rtype"]
        item.recycled_product = rtype
        item.save()
        return redirect('ClothForRecycle')
        
    