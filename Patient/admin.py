from django.contrib import admin
from .models import Patient,PatientDocument,Patient_Address_Model,OrderItem,Feedback,Status,Consultancy
# Register your models here.
admin.site.register(Patient)
admin.site.register(PatientDocument)
admin.site.register(Patient_Address_Model)
admin.site.register(OrderItem)
admin.site.register(Feedback)
admin.site.register(Status)
admin.site.register(Consultancy)