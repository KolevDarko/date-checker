from rest_framework import serializers

from api.models import Store, Product, ProductBatch, BatchWarning


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'id_code', 'id']


class ProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = '__all__'


class BatchWarningSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BatchWarning
        fields = ['id', 'product_batch_id', 'priority', 'old_quantity', 'created_on', 'status']
