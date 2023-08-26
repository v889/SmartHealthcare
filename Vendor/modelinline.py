from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import gettext as _
from django.utils.html import mark_safe
from django.contrib import admin
from .models import Product,ProductImage
class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s ' % \
                (image_url, image_url, file_name, _('')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields=["image"]
    readonly_fields = ['image_tag']
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
