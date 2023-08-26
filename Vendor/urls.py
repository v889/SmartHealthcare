from django.urls import path
from .views import *
urlpatterns=[
    path('home',home,name="vendorhomapage"),
    path('Vendor',VendorView.as_view(),name="Vendor"),
    path('Registration',Registration_Page,name="VendorRegistration"),
    path('OTP',ValidatePhoneSendOTP.as_view(),name="VendorOtp"),
    path('VerifyOtp',VerifyPhoneOTPView.as_view(),name="ValidateOtp"),
    path('address/<int:id>',AddressView.as_view(),name="Address"),
    path('bank/<int:id>',BankView.as_view(),name="Bank"),
    path('Product/<int:id>',ProductView,name="product"),
    path('AddProduct/<int:id>',product_create_view,name='addproduct'),
    path('Logout/<int:id>',Logout,name="logout"),
    path('Order_view/<int:id>',Order_view,name="Order_view")



]