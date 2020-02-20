from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.utils import json

from api.models import BatchWarning, ProductBatchArchive
from api.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(company_id=self.request.user.company_id)


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(company_id=self.request.user.company_id)


class ProductBatchViewSet(viewsets.ModelViewSet):
    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super(ProductBatchViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return ProductBatch.objects.filter(product__company_id=self.request.user.company_id)


class BatchWarningViewSet(viewsets.ModelViewSet):
    queryset = BatchWarning.objects.all()
    serializer_class = BatchWarningSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(BatchWarningViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return BatchWarning.objects.filter(product_batch__product__company_id=self.request.user.company_id)


class ActiveBatchWarningsView(views.APIView):

    def get(self, request):
        active_warnings = BatchWarning.get_active(request.user.store_id)
        return Response(active_warnings)


class ProductsSyncView(views.APIView):

    def get(self, request, product_id):
        new_products = Product.products_after(request.user.company_id, int(product_id))
        serializer = ProductSerializer(new_products, many=True)
        return Response(serializer.data)


class ProductBatchSyncView(views.APIView):
    """
     Uploads new product batches and returns ids for them
    """

    def post(self, request):
        # todo test
        serialized = ProductBatchSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return JsonResponse(status=400, data={'errors': serialized.errors})

class ProductBatchUpdate(views.APIView):
    """
    Updates quantity of product batch and silences warnings
    """

    def update_warning(self, batch_data):
        batch_warning = BatchWarning.get_by_id(batch_data.warning_id)
        batch_warning.mark_checked(batch_data.quantity)
        BatchWarning.silence_warnings(batch_data.batch_id)

    def update_batch(self, batch_data):
        batch = ProductBatch.get_by_id(batch_data.batch_id)
        batch.update_quantity(batch_data.quantity)
        if batch_data.quantity == 0:
            ProductBatchArchive.archive_batch(batch)

    def post(self, request):
        # todo test
        batch_data = json.loads(request.body)
        self.update_batch(batch_data)
        self.update_warning(batch_data)
        return HttpResponse()
