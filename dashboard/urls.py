from django.conf.urls import url

from .views import AddProduct, ProductList

urlpatterns = [
    url(r'product-list$', ProductList.as_view(), name='dash-product-list'),
    url(r'product-add$', AddProduct.as_view(), name='dash-product-add'),
]
