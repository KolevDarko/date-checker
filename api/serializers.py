from rest_framework import serializers

from api.models import Store, Product, ProductInStore


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductInStoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductInStore
        fields = '__all__'
