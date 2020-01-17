from django.db import models

class ModelMixin():

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)

class Store(models.Model, ModelMixin):
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class Product(models.Model, ModelMixin):
    name = models.CharField(max_length=300)
    price = models.FloatField()

class ProductInStore(models.Model, ModelMixin):

    store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='product_items')
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='products_in_store')
    quantity = models.IntegerField()
    expiration_date = models.DateField()
