from rest_framework import viewsets, views
from rest_framework.response import Response

from api.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ProductBatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer

class ProductsSyncView(views.APIView):

    def get(self, request, product_id):
        # new_products = Product.products_after(request.user.company_id, product_id)
        new_products = Product.products_after(1, int(product_id))
        serializer = ProductSerializer(new_products, many=True)
        return Response(serializer.data)
