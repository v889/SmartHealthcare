from django.db import models

# Create your models here.

from django.utils.html import mark_safe
from PIL import Image as Im


class Vendor(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=8)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10)
    license_number=models.CharField(max_length=15)
    issue_authority_name=models.CharField(max_length=1000)
    aadhar_card_number=models.CharField(max_length=12)
    otp=models.IntegerField(null=True,default=None)
    is_authorize=models.BooleanField(default=False)
    has_bankdetails=models.BooleanField(default=False)
    has_shopdetails=models.BooleanField(default=False)
    profile_pic = models.ImageField(default='Profile.png')
    def __str__(self):
        return self.name
class Bank_details(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_bank')
    bank_name=models.CharField(max_length=1024)
    ifsc_code=models.CharField(max_length=1024)
    account_number=models.CharField(max_length=20)


class Address(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_address')
    business_name = models.CharField(max_length=2000)
    adress1=models.CharField(max_length=2000)
    adress2 = models.CharField(max_length=2000)
    Building_Number=models.IntegerField()
    zip_code=models.CharField(max_length=2000)
    city=models.CharField(max_length=2000)
    state=models.CharField(max_length=1024)
    country=models.CharField(max_length=2000)
class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.name
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_products')
    name=models.CharField(max_length=1024)
    price=models.DecimalField(max_digits=7,decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    discount=models.DecimalField(default=0,decimal_places=2,max_digits=5)
    is_apporoved=models.BooleanField(default=False)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products();
class ProductImage(models.Model):
    image=models.FileField(null=True,blank=True)#,upload_to="news/images"
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name="product_image_model")
    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))

    image_tag.short_description = 'Image Preview'

    def save(self):  # new
        super().save()
