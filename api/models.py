from django.db import models

class Store(models.Model):
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField()

class ProductInStore(models.Model):

    store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='product_items')
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='products_in_store')
    quantity = models.IntegerField()
    expiration_date = models.DateField()
