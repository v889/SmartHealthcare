from django.shortcuts import render,redirect
from .models import *
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

# Create your views here.
class DoctorRegisteration(APIView):
    def get(self,request):
        specialization=Specilization.objects.all()
        return render(request,'doctor/registration.html',{'specialization':specialization})
    def post(self,request):
        try:
            print(request.data)
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            email= request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            license_number=request.POST.get('license_number')
            specialist_name=request.POST.get('specialist')
            experience=request.POST.get('experience')
            aadhar_card_number=request.POST.get('aadhar_card_number')
            fees=request.POST.get('fees')
            description=request.POST.get('description')
            issue_authority_name=request.POST.get('issue_authority_name')
            spl = Specilization.objects.get(name=specialist_name)
            doctor=Doctor.objects.create(name=name,
                          gender=gender,
                          email=email,
                          phone_number=phone_number,
                          license_number=license_number,
                          specialist=spl,
                          experience=experience,
                          description=description,
                          aadhar_card_number=aadhar_card_number,
                          issue_authority_name=issue_authority_name,
                           fees=fees)






            return redirect('doctorloginpage')



        except Exception as e:
            messages.warning(request,e)
            return redirect('doctorsignup')
def home(request):
    return render(request,'doctor/index.html')
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
                user = Doctor.objects.filter(phone_number=phone)

                if user.exists():
                    data = user.first()
                    old_otp = data.otp
                    new_otp = send_otp(phone)
                    if old_otp:
                        data.otp = new_otp
                        data.save()
                        messages.success(request,'OTP SENT SUCESSFULLY')
                        return render(request,'doctor/OTP_Verify.html',{'user':data})
                    else:
                        data.otp = new_otp
                        data.save()
                        messages.success(request, 'OTP SENT SUCESSFULLY')
                        return render(request, 'doctor/OTP_Verify.html',{'user':data})

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
                user = Doctor.objects.filter(phone_number=phone)
                print(user[0].otp)

                if str(user[0].otp) == str(otp):
                    request.session['doctor']=user[0].id
                    return render(request,'doctor/home.html',{"user":user[0]})
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

class AddressView(APIView):
    def post(self, request):
        id=request.session['doctor']
        try:

            print(request.data)
            doctor=Doctor.objects.get(pk=id)

            Data=request.data
            d={}
            for x,y in Data.items():
                if(x=='csrfmiddlewaretoken'):
                    continue
                d[x]=y

            print(Data)


            address=Address(doctor=doctor,**d)
            address.save()
            doctor.has_hospitaldetails = True
            doctor.save()
            return render(request,'doctor/home.html',{'user':doctor})



        except Exception as e:
            messages.warning(request,e)
            return render(request,'doctor/home.html',{'user':doctor})

class BankView(APIView):

    def post(self, request):
        id = request.session['doctor']
        try:
            print(request.data)
            doctor=Doctor.objects.get(pk=id)

            Data=request.data
            d={}
            for x,y in Data.items():
                if(x=='csrfmiddlewaretoken'):
                    continue
                d[x]=y

            print(Data)


            bank=Bank_details(doctor=doctor,**d)
            doctor.has_bankdetails = True
            doctor.save()
            bank.save()
            return render(request,'doctor/home.html',{'user':doctor})



        except Exception as e:
            messages.warning(request,e)
            return render(request,'doctor/home.html',{'user':doctor})

def Blog(request):
    id=request.session['doctor']
    doctor=Doctor.objects.get(pk=id)
    return  render(request,'doctor/blogs.html',{'user':doctor})
def blog_create_view(request):
    id = request.session['doctor']
    doctor = Doctor.objects.get(pk=id)
    if request.method == 'POST':
        try:
            title = request.POST.get('name')


            description = request.POST.get('description')
            blogs_image = request.FILES.getlist('images')
            print("Product images",blogs_image)
            blog= Blogs.objects.create(
                create_by=doctor,
                title=title,
                description=description,
            )
            for img in blogs_image:
                print(img)
                image = BlogsImage(image=img,blogs=blog)
                image.save()


            return render(request,'doctor/home.html',{'user':doctor})
        except Exception as e:
            messages.warning(request, e)
            return render(request, 'doctor/blogs.html', {'user': doctor})

