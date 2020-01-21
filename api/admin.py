from django.contrib import admin

# Register your models here.
from .models import ProductInStore, Store, Product

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductInStore)
