from django.conf.urls import url

from .views import AddProduct, HomeView, ExpirationWarning

urlpatterns = [
    url(r'product-list$', HomeView.as_view(), name='dash-product-list'),
    url(r'product-add$', AddProduct.as_view(), name='dash-product-add'),
    url(r'product-expiration$', ExpirationWarning.as_view(), name='dash-warnings'),
]
