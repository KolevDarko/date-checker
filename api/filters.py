import django_filters

from api.models import ProductBatch


class ProductBatchFilter(django_filters.FilterSet):
    # store = django_filters.NumberFilter(field_name='store_id', lookup_expr='iexact')
    # product = django_filters.NumberFilter(field_name='product_id', lookup_expr='iexact')

    class Meta:
        model = ProductBatch
        fields = ['store', 'product']

    # def __init__(self, data, *args, **kwargs):
    #     data = data.copy()
    #     data.setdefault('store', 'paperback')
    #     data.setdefault('order', '-added')
    #     super().__init__(data, *args, **kwargs)
