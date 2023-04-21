from django.urls import path 
from .import views

urlpatterns = [
    path("",views.Index,name="Index"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("RecycleUserCloths",views.RecycleUserCloths,name="RecycleUserCloths"),
    path("UserProfileView",views.UserProfileView,name="UserProfileView"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),
    path("MerchantIndex",views.MerchantIndex,name="MerchantIndex"),  
    
]
