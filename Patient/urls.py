from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name='homepage'),
    path('index/<int:id>',patienthome,name='index'),
    path('sign',RegiterationPage,name='Register'),
    path('Patient',PatientView.as_view(),name='Patient'),
    path('otp',ValidatePhoneSendOTP.as_view(),name='OTP'),
    path('verifyotp',VerifyPhoneOTPView.as_view(),name='verify'),
    path('diabetes/<int:id>',DiabetesForm.as_view(),name="diabetes"),
    path('chronickidney/<int:id>',ChronicKidneyForm.as_view(),name="kidney"),
    path('Heart',HeartForm.as_view(),name="Heart"),
    path('shop',ShopView.as_view(),name="shop"),
    path('doctors/<int:id>',DoctorView.as_view(),name="doctors"),
    path('Profile/<int:id>',ProfileView.as_view(),name="profile"),
    path('Feedback/<int:id>',FeedbackView.as_view(),name="feedback"),
    path('change/<int:id>',ProfilePhotoView.as_view(),name="change"),
    path('cart/<int:id>',CartView.as_view(),name="cart"),
    path('cartadd/<int:id>',CartAddView.as_view(),name='cartadd'),
    path('file/<int:id>',ReportUpload.as_view(),name="reportadd"),
    path('update-attribute/<int:id>/<str:new_value>/', update_attribute, name='update_attribute'),
    path('product_details/<int:id>',product_details,name="Prouct_details"),
    path('productcartadd/<int:id>', ProductCartAddView.as_view(), name='product_cartadd'),
    path('checkout/<int:id>',AddressCheckotView.as_view(),name='checkout'),
    path('address/<int:id>',AddressView.as_view(),name="add_address"),
    path('payment/<int:id>/<int:a_id>',CheckoutView.as_view(),name="checkout_patients"),
    path('order_placed/<int:id>/<int:a_id>/',CodOrderView.as_view(),name="cod_order"),
    path('sucess/order_place/<int:id>/<int:a_id>/<str:razor_order_id>/<str:razor_payment_id>/<str:payment_signature>',OnlinePaymentOrderView.as_view(),name="online_order"),
    path('shop/product_category/<str:category>',cat_product,name="product_cat"),
    path('shop/doctor_category/<str:category>',cat_doctor,name="doctor_cat"),
    path('user/logout',logout,name="patient_logout"),
    path('about',about_view,name='about'),
    path("gmeetings/<int:d_id>",metting,name="gmeetings"),
    path("blogs",blogs,name="blogs"),
    path("blogs_details/<int:id>",blogs_details,name="blogs_details"),
    path("doctor_details/<int:id>",doctor_details,name="doctor_profile"),
    path("order-details/<int:id>",order_details,name="order_details")



]