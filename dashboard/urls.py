from django.conf.urls import url

from .views import AddProductView, CompanyHomeView, ExpirationWarning, ProductListView, ProductBatchAddView, \
    ProductBatchListView, ProductBatchEditView

urlpatterns = [
    url(r'product-list$', ProductListView.as_view(), name='dash-product-list'),
    url(r'product-add$', AddProductView.as_view(), name='dash-product-add'),
    url(r'product-expiration$', ExpirationWarning.as_view(), name='dash-warnings'),
    url(r'product-batch-add$', ProductBatchAddView.as_view(), name='dash-product-batch-add'),
    url(r'product-batch-list/(?P<pk>\w+)$', ProductBatchEditView.as_view(), name='dash-product-batch-edit'),
    url(r'product-batch-list$', ProductBatchListView.as_view(), name='dash-product-batch-list'),
    url(r'', CompanyHomeView.as_view(), name='home'),
]
