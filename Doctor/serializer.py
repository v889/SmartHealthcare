
from rest_framework import serializers
from .models import *

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields='__all__'
class AddressSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(read_only=True, view_name='doctor_address_details')
    class Meta:
        model=Address
        fields='__all__'
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bank_details
        fields='__all__'

