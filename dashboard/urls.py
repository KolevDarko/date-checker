from django.conf.urls import url

from .views import AddProductView, CompanyHomeView, ExpirationWarning, ProductListView

urlpatterns = [
    url(r'product-list$', ProductListView.as_view(), name='dash-product-list'),
    url(r'product-add$', AddProductView.as_view(), name='dash-product-add'),
    url(r'product-expiration$', ExpirationWarning.as_view(), name='dash-warnings'),
    url(r'', CompanyHomeView.as_view(), name='home'),
]
