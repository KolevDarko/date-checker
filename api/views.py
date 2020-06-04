from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.utils import json

from api.controllers import BatchController
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
        last_id = request.GET.get('last_id', None)
        active_warnings = BatchWarning.get_active(request.user.store_id, last_id=last_id)
        return Response(active_warnings)

    def put(self, request):
        data = json.loads(request.body)
        for batch_warning in data['batchWarnings']:
            warning_id = batch_warning['id']
            new_quantity = batch_warning['quantity']
            batch_id = batch_warning['productBatchId']
            BatchController.update_warnings(batch_id, new_quantity)
            BatchController.update_batch(batch_id, new_quantity)
        return JsonResponse({'success': True})


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
        result_batches = []
        for batch_data in request.data:
            new_batch = ProductBatch.create_from_client(batch_data, request.user.store_id)
            result_batches.append(new_batch)
        serialized = ProductBatchSerializer(result_batches, many=True)
        return Response(serialized.data)


    def put(self, request):
        for batch_data in request.data:
            BatchController.update_batch(batch_data['serverId'], batch_data['quantity'])
        return JsonResponse({'success': True}, status=204)
