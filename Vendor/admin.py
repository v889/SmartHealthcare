from django.contrib import admin
from .models import Vendor,Address,Bank_details,Category,Product,ProductImage
from Patient.models import Order
from django.contrib import messages
from .modelinline import *
from django.conf import settings
# Register your models here.
class ProductimageAdmin(admin.ModelAdmin):
    list_display = ["image", "image_tag", "product"] # new

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)
            messages.success(request, 'New Product is added successfully.')
            #self.play_notification_sound()
        else:
            super().save_model(request, obj, form, change)

    list_display = ["name", 'price', 'category','is_apporoved']
    inlines = [ProductImageInline]

    search_fields = ('name', 'price')

    '''def play_notification_sound(self):
        script = '<script>new Audio("{0}/Patient/static/notification.mp3").play();</script>'.format(settings.STATIC_URL)
        self.message_user(self.request, script, extra_tags='safe')'''


admin.site.register(Vendor)
admin.site.register(Address)
admin.site.register(Bank_details)
admin.site.register(Category)
admin.site.register(ProductImage,ProductimageAdmin)
admin.site.register(Order)
