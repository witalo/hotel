from django.contrib import admin

# Register your models here.
from apps.products.models import Product, ProductBrand, ProductStore

admin.site.register(Product)
admin.site.register(ProductBrand)
admin.site.register(ProductStore)