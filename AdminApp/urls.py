from django.urls import path 
from .import views

urlpatterns = [
    path("RecycleRequests",views.RecycleRequests,name="RecycleRequests"),
    path("ApproveReq/<int:pk>",views.ApproveReq,name="ApproveReq"),
    path("RejectReq/<int:pk>",views.RejectReq,name="RejectReq"),
    path("CollectReq/<int:pk>",views.CollectReq,name="CollectReq"),
    path("SentForRecycleReq/<int:pk>",views.SentForRecycleReq,name="SentForRecycleReq"),
    path("RecycledReq/<int:pk>",views.RecycledReq,name="RecycledReq"),
    path("ProductAdmin",views.ProductAdmin,name="ProductAdmin"),
    path("Cart",views.Cart,name="Cart"),
    path("CheckOut",views.CheckOut,name="CheckOut"),
    path("IncreaseCartQunty/<int:pk>",views.IncreaseCartQunty,name="IncreaseCartQunty"),
    path("DecreaseCartQunty/<int:pk>",views.DecreaseCartQunty,name="DecreaseCartQunty"),
    path("DeleteCart/<int:pk>",views.DeleteCart,name="DeleteCart"),
    path("AddTocart/<int:pk>",views.AddTocart,name="AddTocart"),
    path("Myorders",views.Myorders,name="Myorders"),
    path("deleteorderedhistory/<int:pk>",views.deleteorderedhistory,name="deleteorderedhistory"),
    path("Customerorders",views.Customerorders,name="Customerorders"),
    path("ChangeToDespached/<int:pk>",views.ChangeToDespached,name="ChangeToDespached"),
    path("ChangeToDelivered/<int:pk>",views.ChangeToDelivered,name="ChangeToDelivered"),
    path("ChangeToCanceled/<int:pk>",views.ChangeToCanceled,name="ChangeToCanceled"),
    path("DelateOrderMerchant/<int:pk>",views.DelateOrderMerchant,name="DelateOrderMerchant"),
    path("ViewAddress/<int:pk>",views.ViewAddress,name="ViewAddress"),
    path("paymenthandlercus",views.paymenthandlercus,name="paymenthandlercus"),
    path("Checkoutwithpoints",views.Checkoutwithpoints,name="Checkoutwithpoints"),
    path("UplaodTutorialVideos",views.UplaodTutorialVideos,name="UplaodTutorialVideos"),
    path("SearchByName",views.SearchByName,name="SearchByName"),   
    
]
