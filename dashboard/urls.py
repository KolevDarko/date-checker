from django.conf.urls import url

from .views import AddProductView, CompanyHomeView, BatchWarningListView, ProductListView, ProductBatchAddView, \
    ProductBatchListView, ProductBatchEditView, EditProductView

urlpatterns = [
    url(r'product$', ProductListView.as_view(), name='dash-product-list'),
    url(r'product/(?P<pk>\w+)$', EditProductView.as_view(), name='dash-product-edit'),
    url(r'product-add$', AddProductView.as_view(), name='dash-product-add'),
    url(r'product-batch-add$', ProductBatchAddView.as_view(), name='dash-product-batch-add'),
    url(r'product-batch-list/(?P<pk>\w+)$', ProductBatchEditView.as_view(), name='dash-product-batch-edit'),
    url(r'product-batch-list$', ProductBatchListView.as_view(), name='dash-product-batch-list'),
    url(r'batch-warning-list$', BatchWarningListView.as_view(), name='dash-warnings'),
    url(r'', CompanyHomeView.as_view(), name='home'),
]
