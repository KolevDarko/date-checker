from django.conf.urls import url

from .views import AddProduct, HomeView

urlpatterns = [
    url(r'product-list$', HomeView.as_view(), name='dash-product-list'),
    url(r'product-add$', AddProduct.as_view(), name='dash-product-add'),
]
