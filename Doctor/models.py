from django.db import models
from django.utils.html import mark_safe
# Create your models here.
class Specilization(models.Model):
    name=models.CharField(max_length=500)
    def __str__(self):
        return self.name
class Doctor(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=8)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10)
    license_number=models.CharField(max_length=15)
    issue_authority_name=models.CharField(max_length=1000)
    specialist=models.ForeignKey(Specilization,on_delete=models.CASCADE,related_name="doctor_specialist")
    experience=models.IntegerField()
    aadhar_card_number=models.CharField(max_length=12)
    otp=models.IntegerField(null=True,default=None)
    is_authorize=models.BooleanField(default=False)
    has_bankdetails=models.BooleanField(default=False)
    has_hospitaldetails=models.BooleanField(default=False)
    profile_pic = models.ImageField(default='Profile.png')
    fees=models.DecimalField(max_digits=7,decimal_places=3,default=500.000)
    description=models.CharField(max_length=10000)

    def __str__(self):
        return self.name

class Bank_details(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_bank')
    bank_name=models.CharField(max_length=1024)
    ifsc_code=models.CharField(max_length=1024)
    upi_id=models.CharField(max_length=1024,default=None)
    account_number=models.CharField(max_length=20)



class Address(models.Model):
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_address')


    adress1=models.CharField(max_length=2000)
    adress2 = models.CharField(max_length=2000)
    Building_Number=models.IntegerField()
    zip_code=models.CharField(max_length=2000)
    city=models.CharField(max_length=2000)
    state=models.CharField(max_length=1024)
    country=models.CharField(max_length=2000)
class Blogs(models.Model):
    create_by=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="doctor_blogs")
    title=models.CharField(max_length=3000)
    description=models.CharField(max_length=1000000)
    is_apporved=models.BooleanField(default=False)
class BlogsImage(models.Model):
    image=models.FileField(null=True,blank=True)#,upload_to="news/images"
    blogs=models.ForeignKey(Blogs,on_delete=models.CASCADE,null=True,blank=True,related_name="blogs_image_model")
    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))

    image_tag.short_description = 'Image Preview'

    def save(self):  # new
        super().save()