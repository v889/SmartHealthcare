
from rest_framework import serializers
from .models import *
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
class VenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'
class AddressSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(read_only=True, view_name='course-detail')
    class Meta:
        model=Address
        fields='__all__'
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bank_details
        fields='__all__'


