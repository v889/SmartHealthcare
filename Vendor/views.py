from django.shortcuts import render,redirect
from .models import Product
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
from Patient.utils import otp_generator
from rest_framework import status
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from sms import send_sms
from Patient.models import OrderItem
# Create your views here.


def home(request):
    return render(request,'vendor/home.html')
def product_create_view(request,id):
    vendor=Vendor.objects.get(pk=id)
    category=Category.objects.all()
    if request.method == 'POST':
        try:
            product_name = request.POST.get('name')
            product_price = request.POST.get('price')
            product_category=request.POST.get('category')
            product_description = request.POST.get('description')
            product_image = request.FILES.getlist('images')
            print("Product images",product_image)
            cat=Category.objects.get(name=product_category)
            product = Product.objects.create(
                name=product_name,
                price=product_price,
                category=cat,
                vendor=vendor,
                description=product_description
            )
            for img in product_image:
                print(img)
                image = ProductImage(image=img,product=product)
                image.save()


            return render(request,'vendor/index.html',{'user':vendor})
        except Exception as e:
            messages.warning(request, e)
            return render(request, 'vendor/product.html', {'user': vendor,'Category':category})

def Registration_Page(request):
    return  render(request,'vendor/registration.html')
class VendorView(APIView):
    def get(self, request):
        vendor = Vendor.objects.all()
        serializer =VenderSerializer (vendor, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            print(request.data)

            serializer = VenderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('vendorhomapage')

            else:
                messages.warning(request, "Something bad happend, try again later.")
                return  redirect('VendorRegistration')

        except Exception as e:
            messages.warning(request,e)
            return redirect('VendorRegistration')

class AddressView(APIView):
    def post(self, request,id):
        try:
            print(request.data)
            vendor=Vendor.objects.get(pk=id)

            Data=request.data
            d={}
            for x,y in Data.items():
                if(x=='csrfmiddlewaretoken'):
                    continue
                d[x]=y

            print(Data)


            address=Address(vendor=vendor,**d)
            address.save()
            vendor.has_shopdetails = True
            vendor.save()
            return render(request,'vendor/index.html',{'user':vendor})



        except Exception as e:
            messages.warning(request,e)
            return render(request,'vendor/index.html',{'user':vendor})

class BankView(APIView):
    def post(self, request,id):
        try:
            print(request.data)
            vendor=Vendor.objects.get(pk=id)

            Data=request.data
            d={}
            for x,y in Data.items():
                if(x=='csrfmiddlewaretoken'):
                    continue
                d[x]=y

            print(Data)


            bank=Bank_details(vendor=vendor,**d)
            vendor.has_bankdetails = True
            vendor.save()
            bank.save()
            return render(request,'vendor/index.html',{'user':vendor})



        except Exception as e:
            messages.warning(request,e)
            return render(request,'vendor/index.html',{'user':vendor})


def send_otp(phone):


    if phone:

        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)




        link = f'https://2factor.in/API/V1/6a04b8dc-d9eb-11ed-addf-0200cd936042/SMS/91{phone}/{otp_key}'
        result = requests.get(link, verify=False)

        return otp_key
    else:
        return False


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *agrs, **kwargs):
        try:
            phone_number = request.data.get('phone')

            if phone_number:
                phone = str(phone_number)
                user = Vendor.objects.filter(phone_number=phone)

                if user.exists():
                    data = user.first()
                    old_otp = data.otp
                    new_otp = send_otp(phone)
                    if old_otp:
                        data.otp = new_otp
                        data.save()
                        messages.success(request,'OTP SENT SUCESSFULLY')
                        return render(request,'vendor/OTP_Verify.html',{'user':data})
                    else:
                        data.otp = new_otp
                        data.save()
                        messages.success(request, 'OTP SENT SUCESSFULLY')
                        return render(request, 'vendor/OTP_Verify.html',{'user':data})

                else:
                    return Response({
                        'message': 'User not found ! please register',
                        'status': status.HTTP_404_NOT_FOUND,
                    }
                    )
            else:
                return Response({
                    'message': 'Phone number is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                })
        except Exception as e:
            return Response({
                'message': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
            })



class VerifyPhoneOTPView(APIView):
    def post(self, request, format=None):
        try:
            phone = request.data.get('phone')
            otp = request.data.get('otp')
            #otp=int(otp)
            print(phone, otp)

            if phone and otp:
                user = Vendor.objects.filter(phone_number=phone)
                print(user[0].otp)

                if str(user[0].otp) == str(otp):
                    return render(request,'vendor/index.html',{'user':user[0]})
                else:
                    return Response({'message': 'OTP does not match'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'message': 'Phone or OTP is missing'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': str(e),
                'details': 'Login Failed'
            })

def ProductView(request,id):
    vendor=Vendor.objects.get(pk=id)
    cat=Category.objects.all()
    return render(request,'vendor/product.html',{'Category':cat,'user':vendor})


def Logout(request,id):
    vendor=Vendor.objects.get(pk=id)
    vendor.otp=None
    return render(request,'vendor/Home.html')

def Order_view(request,id):
    vendor= Vendor.objects.get(pk=id)
    order=OrderItem.objects.all()
    print(order)

    for i in order:
        print(i.product.vendor.id,vendor.id)
        if(i.product.vendor.id!=vendor.id):
            order.pop(i)
    print(order)
    return  render(request,'vendor/order_view.html',{'user':vendor,'orders':order})
def product_view(request,id):
    user = Vendor.objects.get(pk=id)
    product=Product.objects.filter(vendor=user)
    return  render(request,'vendor/products.html',{"user":user,"orders":product})
