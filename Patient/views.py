from django.shortcuts import render,redirect
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.core.paginator import Paginator

import joblib
from django.conf import settings
import uuid
from Vendor.models import *
from rest_framework import mixins,generics
from .models import *
from .serializer import PatientSerializer
from rest_framework import status
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .utils import otp_generator
from django.http import JsonResponse
from django.urls import reverse
import pickle
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf.pisa import pisaDocument
from django.http import FileResponse,HttpResponse
from Doctor.models import *
from .apps import PatientConfig
import razorpay
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, time, timedelta
# Create your views here.
class ProfileView(APIView):
    def get(self,request,id):
        user=Patient.objects.get(pk=id)
        reports=user.patient_documents.all()
        consultancy=Consultancy.objects.filter(patient=user)
        print(consultancy)
        print(reports)
        orders=Order.objects.filter(customer=user)
        for i in orders:
            print(len(i.items.all()))

        return render(request,'profile.html',{'user':user,'reports':reports,'orders':orders,"cosnltancy":consultancy})
class ShopView(APIView):
    def get(self,request):
        id = request.session['patient']
        user=Patient.objects.get(pk=id)
        products=Product.objects.filter(is_apporoved=True)
        p = Paginator(products, 10)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        categories=Category.objects.all()
        return render(request,'shop.html',{'products':page_obj,'user':user,'categories':categories})
class DoctorView(APIView):
    def get(self,request,id):
        user=Patient.objects.get(pk=id)
        doctors=Doctor.objects.filter(is_authorize=True)
        specilization=Specilization.objects.all()
        return render(request,'doctor.html',{'doctors':doctors,'user':user,'specialization':specilization})
def home(request):
    return render(request,'index.html')
def patienthome(request,id):
    user=Patient.objects.get(pk=id)
    products=Product.objects.all()
    feedback=Feedback.objects.filter(on_screen=True)
    return render(request, 'home.html',{'products':products,'user':user,'feedbacks':feedback})
def RegiterationPage(request):
    return render(request,'Registeration.html')
class PatientView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    def get(self,request):

        return self.list(request)

    def post(self, request):

        try:

            self.create(request)
            messages.success(request,"You Registration Sucessfully")
            return render(request,'index.html')
        except:
            messages.warning(request, "Something bad happend, try again later.")
            return render(request,'Registeration.html')


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
                user = Patient.objects.filter(phone_number=phone)

                if user.exists():
                    data = user.first()
                    old_otp = data.otp
                    new_otp = send_otp(phone)
                    if old_otp:
                        data.otp = new_otp
                        data.save()
                        messages.success(request,'OTP SENT SUCESSFULLY')
                        return render(request,'OTP_Verify.html',{'user':data})
                    else:
                        data.otp = new_otp
                        data.save()
                        messages.success(request, 'OTP SENT SUCESSFULLY')
                        return render(request, 'OTP_Verify.html',{'user':data})

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
                user = Patient.objects.filter(phone_number=phone)
                print(user[0].otp)

                if str(user[0].otp) == str(otp):
                    products=Product.objects.filter(is_apporoved=True)
                    request.session['patient'] = user[0].id

                    return render(request,'home.html',{"products":products,'user':user[0]})
                else:
                    messages.warning(request,"OTP DOES NOT  MATCH")
                    return render(request,'OTP_Verify.html',{'user':user[0]})

            else:
                return Response({'message': 'Phone or OTP is missing'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': str(e),
                'details': 'Login Failed'
            })
import datetime
def diabetes_pdf(params:dict):
    template=get_template('diabetesPdf.html')
    html=template.render(params)
    response=BytesIO()
    pdf=pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name=uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR)+f'/media/{file_name}.pdf','wb+') as output:
            pdf=pisaDocument(BytesIO(html.encode('UTF-8')),output)
    except Exception as e:
        print(e)
    if pdf.err:
        return '',False
    return file_name,True
def kidney_pdf(params:dict):
    template=get_template('kidneyPdf.html')
    html=template.render(params)
    response=BytesIO()
    pdf=pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name=uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR)+f'/media/{file_name}.pdf','wb+') as output:
            pdf=pisaDocument(BytesIO(html.encode('UTF-8')),output)
    except Exception as e:
        print(e)
    if pdf.err:
        return '',False
    return file_name,True
def Heart_pdf(params:dict):
    template=get_template('HeartPdf.html')
    html=template.render(params)
    response=BytesIO()
    pdf=pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name=uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR)+f'/media/{file_name}.pdf','wb+') as output:
            pdf=pisaDocument(BytesIO(html.encode('UTF-8')),output)
    except Exception as e:
        print(e)
    if pdf.err:
        return '',False
    return file_name,True
class DiabetesForm(APIView):
    def get(self,request,id):
        user=Patient.objects.get(pk=id)

        return render(request,"diabetes.html",{'user':user})
    def post(self,request,id):
        user = Patient.objects.get(pk=id)
        print(PatientConfig.MLFOLDER)
        print(PatientConfig.MODEL_FILE)
        lr = pickle.load(open("C:/Users/DELL/Downloads/diabetes_model (1).sav",'rb'))
        Pregnancies=request.data['Pregnancies']
        Glucose=request.data['Glucose']
        BloodPressure=request.data['BloodPressure']
        SkinThickness=request.data['SkinThickness']
        Insulin=request.data['Insulin']
        BMI=request.data['BMI']
        DiabetesPedigreeFunction=request.data['DiabetesPedigreeFunction']
        Age=request.data['Age']


        ans = lr.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])[0]
        print(ans)
        Result=""
        if(ans==0):
            Result="Person has no diabetes"
        else:
            Result="Person has diabetes"
        params={
            'Age':Age,
            'Glucose':Glucose,
            'BMI':BMI,
            'Insulin':Insulin,
            'BloodPressure':BloodPressure,
            'Pregnancies':Pregnancies,
            'user':user,
            'Result':Result


        }
        file_name,status=diabetes_pdf(params)
        file=str(settings.BASE_DIR) + f'/media/{file_name}.pdf'
        response = FileResponse(open(file, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}".format(file_name)
        return response
import joblib
import  numpy as np
class HeartForm(APIView):
    def get(self,request):
        pid = request.session['patient']
        user = Patient.objects.get(pk=pid)
        return  render(request,'HeartDisease.html',{'user':user})
    def post(self,request):
        pid = request.session['patient']
        user = Patient.objects.get(pk=pid)
        print(PatientConfig.MLFOLDER)
        print(PatientConfig.MODEL_FILE)
        lr = joblib.load("C:/Users/DELL/PycharmProjects/SmartHealthCare/models/heart_disease.h5")
        age = request.data['Age']
        sex = request.data['Sex']
        cp = request.data['Cp']
        trestps =request.data['Rbp']
        chol = request.data['Chol']
        fbs = request.data['Fbs']
        restecq = request.data['Recg']
        thalach = request.data['Tach']
        exang = request.data['Exang']
        oldpeak = request.data['Opeak']
        slope = request.data['Slope']
        ca = request.data['Ca']
        thal = request.data['Thal']

        a = [age, sex, cp, trestps, chol, fbs, restecq, thalach, exang, oldpeak, slope, ca, thal]

        b = np.array(a, dtype=float)  # convert using numpy
        c = [float(i) for i in a]

        ans = lr.predict([c])[0]
        print(ans)
        Result=""
        if(ans==0):
            Result="Healthy Heart"
        else:
            Result="Defective Heart"
        params={
            'Age':age,
            'Chol':chol,
            'Result':Result,
            'Fbs':fbs,
            'Cp':cp,
            'Restbp':trestps,
            'user':user,
            'Sex':sex





        }
        file_name,status=Heart_pdf(params)
        file=str(settings.BASE_DIR) + f'/media/{file_name}.pdf'
        response = FileResponse(open(file, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}".format(file_name)
        return response


class ChronicKidneyForm(APIView):
    def get(self,request,id):
        user=Patient.objects.get(pk=id)

        return render(request,"ChronicKidney.html",{'user':user})
    def post(self,request,id):
        user = Patient.objects.get(pk=id)
        print(PatientConfig.MLFOLDER)
        print(PatientConfig.MODEL_FILE)
        lr = pickle.load(open("C:/Users/DELL/Downloads/kidney.sav",'rb'))
        sg=request.data['SG']
        al=request.data['AL']
        sc=request.data['SC']
        hemo=request.data['Hemo']
        pcv=request.data['Pcv']
        htn=request.data['Htn']



        ans = lr.predict([[sg,al,sc,hemo,pcv,htn]])[0]
        if (ans == 0):
            Result = "Person has no chornic kidney"
        else:
            Result = "Person has chornic kidney"
        params = {
            'Sg': sg,
            'AL': al,
            'SC': sc,
            'Hemo': hemo,
            'Pcv': pcv,
            'user': user,
            'Result': Result

        }
        file_name, status = kidney_pdf(params)
        file = str(settings.BASE_DIR) + f'/media/{file_name}.pdf'
        response = FileResponse(open(file, 'rb'), content_type="application/pdf")
        response["Content-Disposition"] = "filename={}".format(file_name)
        return response

class FeedbackView(APIView):
    def get(self,request,id):
        user=Patient.objects.get(pk=id)
        return render(request,'feedback.html',{'user':user})
    def post(self,request,id):
        user=Patient.objects.get(pk=id)
        Message=request.data['Message']
        feedback=Feedback(patient=user,Message=Message)
        email = EmailMessage(
            subject="Thank for your feedback",
            body=f"HII {user.name},\n Thanks for choosing smarthealthcare app.Your feedback is important for us.",
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.send()
        feedback.save()
        messages.success(request,"Your Feedback send successfully")
        return render(request,'feedback.html',{"user":user})
class ProfilePhotoView(APIView):
    def post(self,request,id):
        user=Patient.objects.get(pk=id)
        image = request.FILES.get('images')
        print(image)
        user.profile_pic=image
        user.save()
        messages.success(request,"Your Photo update sucessfully")
        return  render(request,'profile.html',{"user":user})
class CartView(APIView):
    def get(self,request,id):
        ids = list(request.session.get('cart').keys())
        print("id",ids)
        button=True

        products = Product.get_products_by_id(ids)
        if(len(products)==0):
            button=False

        print("products",products)

        user = Patient.objects.get(pk=id)
        return  render(request,'cart2.html',{'user':user,"products":products,'b':button})
class AddressCheckotView(APIView):
    def get(self,request,id):
        user = Patient.objects.get(pk=id)
        address=user.patient_address.all()
        return render(request, 'checkout.html', {'user': user, "addresses":address})
from django.conf import settings

from decimal import Decimal


razorpay_client = razorpay.Client(auth=("rzp_test_hMrfgdaniViVVZ","enPCcIi23GvQA6rg1MIEk8qU"))
class CheckoutView(APIView):
    def get(self,request,id,a_id):
        ids = list(request.session.get('cart').keys())
        address=Patient_Address_Model.objects.get(pk=a_id)

        print("id", ids)
        products = Product.get_products_by_id(ids)
        print("products", products)
        request.session['address']=address.id
        amount= 0
        for p in products:
            amount += p.price
        amount=int(amount)*100
        payment = razorpay_client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})


        user = Patient.objects.get(pk=id)
        return render(request, 'checkout2.html', {'user': user, "products": products,"address":address,'payment':payment})


class CodOrderView(APIView):
    def get(self,request,id,a_id):
        customer=Patient.objects.get(pk=id)

        address = Patient_Address_Model.objects.get(pk=a_id)
        ids = list(request.session.get('cart').keys())
        # print("id", ids)
        products = Product.get_products_by_id(ids)

        try:
            sum = 0
            for p in products:
                sum += p.price
            order=Order(address=address, customer=customer,number_of_product=len(products),total_bill=sum)
            order.save()
            cart=request.session.get('cart')
            for p in products:
                temp=str(p.id)
                q=cart.get(temp)
                OrderItem.objects.create(order=order,product=p,quantity=q)
            request.session['address']=None
            request.session['cart']={}

            email = EmailMessage(
                subject="Order Conformation",
                body=f"HII {customer.name},\n Thanks for choosing smarthealthcare app.Your Order on the Way.",
                from_email=settings.EMAIL_HOST_USER,
                to=[customer.email],
            )
            email.send()
            return render(request,'thankyou.html',{'user':customer})
        except Exception as e:
            messages.warning(request,e)

            return render(request, 'checkout2.html', {'user': customer, "products": products})


class OnlinePaymentOrderView(APIView):
    def get(self, request, id, a_id,razor_order_id,razor_payment_id,payment_signature):
        customer = Patient.objects.get(pk=id)

        address = Patient_Address_Model.objects.get(pk=a_id)
        ids = list(request.session.get('cart').keys())
        # print("id", ids)
        products = Product.get_products_by_id(ids)

        try:
            sum = 0
            for p in products:
                sum += p.price
            order = Order(address=address, customer=customer, number_of_product=len(products), total_bill=sum,payment_done=True)
            order.save()
            cart = request.session.get('cart')
            for p in products:
                temp = str(p.id)
                q = cart.get(temp)
                OrderItem.objects.create(order=order, product=p, quantity=q)
            OnlinePayment=OnlinePaymentDetails(order=order,razor_pay_order_id=razor_order_id,razor_pay_payment_id=razor_payment_id,razor_pay_payment_signature=payment_signature)
            OnlinePayment.save()
            request.session['address'] = None
            request.session['cart'] = {}
            return render(request, 'thankyou.html', {'user': customer})
        except Exception as e:
            messages.warning(request, e)

            return render(request, 'checkout2.html', {'user': customer, "products": products})


class CartAddView(APIView):
    def post(self , request,id):
        products=Product.objects.all()
        user=Patient.objects.get(pk=id)
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return render(request,'home.html',{'user':user,'products':products})

class ProductCartAddView(APIView):
    def post(self , request,id):
        user=Patient.objects.get(pk=id)
        product= request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print(product)
        pid=int(product)
        products= Product.objects.get(pk=pid)
        product_images = products.product_image_model.all()
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])

        return render(request, 'shop-single.html', {"product": products, 'product_images': product_images,"user":user})


class ReportUpload(APIView):
    def post(self,request,id):
        user = Patient.objects.get(pk=id)
        name=request.data.get('Name')
        file= request.FILES.get('file')
        try:
            patientdoc=PatientDocument(patient=user,name=name,file=file)
            patientdoc.save()
            messages.success(request, "Your Report update sucessfully")
            return render(request, 'profile.html', {"user": user})
        except:
            messages.warning(request, "Something bad happend, try again later.")
            return render(request,'profile.html', {"user": user})

class AddressView(APIView):
    def post(self, request,id):
        patient = Patient.objects.get(pk=id)
        address=patient.patient_address.all()

        try:

            print(request.data)


            Data=request.data
            d={}
            for x,y in Data.items():
                if(x=='csrfmiddlewaretoken'):
                    continue
                d[x]=y

            print(Data)


            add=Patient_Address_Model(patient=patient,**d)
            add.save()
            return render(request,'checkout.html',{'user':patient,'addresses':address})



        except Exception as e:
            messages.warning(request,e)
            return render(request,'checkout.html',{'user':patient,'addresses':address})
def update_attribute(request, id, new_value):
    try:
        print(id)
        obj = PatientDocument.objects.get(id=id)
        print(obj)
        if(new_value=='false'):
            obj.show_doctor = False
        else:
            obj.show_doctor = True

        obj.save()


        return JsonResponse({'success': True})
    except PatientDocument.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Object not found'})

def product_details(request,id):
    product=Product.objects.get(pk=id)
    product_images=product.product_image_model.all()
    id = request.session['patient']
    user = Patient.objects.get(pk=id)
    return render(request,'shop-single.html',{"product":product,'product_images':product_images,'user':user})

def cat_product(request,category):
    cat=Category.objects.get(name=category)
    products=Product.objects.filter(category=cat)
    print(products)
    id=request.session['patient']
    user=Patient.objects.get(pk=id)
    category=Category.objects.all()
    p = Paginator(products, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request,'shop.html',{'user':user,'products':page_obj,'categories':category})
def cat_doctor(request,category):
    spl=Specilization.objects.get(name=category)
    specialization=Specilization.objects.all()
    doctors=Doctor.objects.filter(specialist=spl)
    id=request.session['patient']
    user=Patient.objects.get(pk=id)

    return render(request,'doctor.html',{'user':user,'doctors':doctors,'specialization':specialization})
def logout(request):
    id = request.session['patient']
    user = Patient.objects.get(pk=id)
    user.otp=None
    request.session['patient']=None
    return render(request,'index.html')
def about_view(request):
    id = request.session['patient']
    user = Patient.objects.get(pk=id)
    return  render(request,'about.html',{'user':user})
import time
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
def metting(request,d_id):

    doctor=Doctor.objects.get(pk=d_id)
    id = request.session['patient']
    user = Patient.objects.get(pk=id)
    participant1_email = user.email
    participant2_email = doctor.email
    new_counst=Consultancy.objects.create(patient=user,doctor=doctor)
    new_counst.save()
    email = EmailMessage(
        subject="New Patient Request",
        body=f"HII {doctor.name},\n New patient request for you.User {user.name} have book appointment with you.\n Please contact on {user.email} or {user.phone_number}",
        from_email=settings.EMAIL_HOST_USER,
        to=[participant2_email],
    )

    # Attach the PDF file
    documents=PatientDocument.objects.filter(patient=user,show_doctor=True)
    print(documents)
    for i in documents:
        email.attach(i.name, i.file.read(), 'application/pdf')
    email.send()
    return render(request, 'thankyou.html',{"user":user})

def blogs(request):
    id = request.session['patient']
    user = Patient.objects.get(pk=id)
    blogs=Blogs.objects.filter(is_apporved=True)
    p = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return  render(request,'blog.html',{'user':user,'blogs':page_obj})
def blogs_details(request,id):
    pid= request.session['patient']
    user = Patient.objects.get(pk=pid)
    products = Product.objects.filter(is_apporoved=True)

    blog=Blogs.objects.get(pk=id)
    blogs_image=blog.blogs_image_model.all()

    return  render(request,"blogs_detail.html",{'user':user,'news':blog,'news_images':blogs_image,'products':products})

def doctor_details(request,id):
    pid = request.session['patient']
    user = Patient.objects.get(pk=pid)
    doctor=Doctor.objects.get(pk=id)

    products = Product.objects.filter(is_apporoved=True)
    return  render(request,"doctor_profile.html",{"user":user,"person":doctor,"products":products})

def order_details(request,id):
    order=Order.objects.get(pk=id)
    pid = request.session['patient']
    user = Patient.objects.get(pk=pid)
    orders=order.items.all()
    return render(request,"order.html",{"user":user,"orders":orders})





