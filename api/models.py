from django.db import models
from django.conf import settings

class ModelMixin():

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)

class Company(models.Model):
    name = models.CharField(max_length=200)

class Store(models.Model, ModelMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_stores')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class Product(models.Model, ModelMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_products')
    name = models.CharField(max_length=300)
    price = models.FloatField()
    id_code = models.CharField(max_length=100)

class ProductBatch(models.Model, ModelMixin):

    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='store_batches')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_batches')
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    id_code = models.CharField(max_length=100)

class BatchWarning(models.Model):

    STATUS_NEW = 'NEW'
    STATUS_CHECKED = 'CHECKED'

    PRIORITY_WARNING = 'WARNING'
    PRIORITY_EXPIRED = 'EXPIRED'


    product_batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, related_name='batch_warnings')
    status = models.CharField(max_length=10, default=STATUS_NEW)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    priority = models.CharField(max_length=10, default=PRIORITY_WARNING)
