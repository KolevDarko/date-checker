from rest_framework import viewsets, views
from rest_framework.response import Response

from api.models import BatchWarning
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

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(ProductBatchViewSet, self).get_serializer(*args, **kwargs)


class BatchWarningViewSet(viewsets.ModelViewSet):
    queryset = BatchWarning.objects.all()
    serializer_class = BatchWarningSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(BatchWarningViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        pass

class ProductsSyncView(views.APIView):

    def get(self, request, product_id):
        # todo, fix after authenticaiton
        # new_products = Product.products_after(request.user.company_id, product_id)
        new_products = Product.products_after(1, int(product_id))
        serializer = ProductSerializer(new_products, many=True)
        return Response(serializer.data)
