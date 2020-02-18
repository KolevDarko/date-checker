from rest_framework import serializers

from api.models import Store, Product, ProductBatch


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'id_code', 'id']

class ProductBatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductBatch
        fields = '__all__'
