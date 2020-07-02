from django.contrib import admin
from .models import Brand, Product
# Register your models here.

admin.site.register(Brand)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'created_at', 'updated_at')
admin.site.register(Product, ProductAdmin)
