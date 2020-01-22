from django.db import models
from django.conf import settings

class ModelMixin():

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)

class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='user_companies')
    name = models.CharField(max_length=200)

class Store(models.Model, ModelMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_stores')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class Product(models.Model, ModelMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_products')
    name = models.CharField(max_length=300)
    price = models.FloatField()
    barcode = models.CharField(max_length=100)

class ProductInStore(models.Model, ModelMixin):

    store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='store_batches')
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_batches')
    quantity = models.IntegerField()
    expiration_date = models.DateField()
