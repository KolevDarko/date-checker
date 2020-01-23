from django.contrib import admin

# Register your models here.
from .models import ProductBatch, Store, Product, Companies

admin.site.register(Companies)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductBatch)
