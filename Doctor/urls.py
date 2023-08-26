from .views import *
from django.urls import path
urlpatterns=[
    path('login', home, name="doctorloginpage"),
    path('signup',DoctorRegisteration.as_view(),name="doctorsignup"),
    path('OTP',ValidatePhoneSendOTP.as_view(),name="DoctorOtp"),
    path('VerifyOtp',VerifyPhoneOTPView.as_view(),name="ValidateDoctorOtp"),
    path('address',AddressView.as_view(),name="DoctorAddress"),
    path('bank',BankView.as_view(),name="DoctorBank"),
    path('blogs',Blog,name="Blogs"),
    path('blog_create',blog_create_view,name="blogs_create"),
]
