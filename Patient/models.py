from django.db import models
from Doctor.models import *
from django.contrib.auth.models import User
from Vendor.models import *
# Create your models here.
class Patient(models.Model):
    name=models.CharField(max_length=80)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10)
    age=models.IntegerField()
    gender=models.CharField(max_length=50)
    otp=models.IntegerField(null=True,default=None)
    profile_pic=models.ImageField(default='Profile.png')
    def __str__(self):
        return self.name
class Feedback(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE, related_name='patient_feedbacks')
    Message=models.TextField()
    on_screen=models.BooleanField(default=False)
class PatientDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_documents')
    name=models.CharField(max_length=1024)
    file = models.FileField()
    show_doctor = models.BooleanField(default=False)
class ChatSession(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatImage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chat_images')
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatPDF(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='chat_pdfs')
    timestamp = models.DateTimeField(auto_now_add=True)

class Patient_Address_Model(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_address')
    first_name = models.CharField(max_length=2000)
    last_name = models.CharField(max_length=2000)
    village_or_colony= models.CharField(max_length=2000)
    landmark=models.CharField(max_length=3000)
    Building_Number=models.IntegerField()
    zip_code=models.CharField(max_length=2000)
    city=models.CharField(max_length=2000)
    state=models.CharField(max_length=1024)
    country=models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=10)
class Status(models.Model):
    name=models.CharField(max_length=500)
    def __str__(self):
        return self.name
import datetime
class Order(models.Model):
    address=models.ForeignKey(Patient_Address_Model,on_delete=models.CASCADE,related_name='order_address')
    customer=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='order_customer')
    number_of_product = models.IntegerField()
    total_bill= models.DecimalField(max_digits=7, decimal_places=3)
    admin_verify=models.BooleanField(default=False)
    vendor_verify=models.BooleanField(default=False)
    payment_done=models.BooleanField(default=False)
    date = models.DateField(default=datetime.datetime.today)
    status=models.ForeignKey(Status,on_delete=models.CASCADE,related_name='order_status',null=True,default=None)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    verify=models.BooleanField(default=False)
class OnlinePaymentDetails(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="online_order_paymnet")
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
class Consultancy(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="Patient_consultancy")
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="Doctor_consultancy")
    date = models.DateField(default=datetime.datetime.today)