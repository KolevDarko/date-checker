"""datecheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api import views
from rest_framework.authtoken import views as auth_views

from dashboard.views import CompanyHomeView, BatchWarningListView

router = routers.DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product-batches', views.ProductBatchViewSet, basename='product-batch')
router.register(r'batch-warnings', views.BatchWarningViewSet, basename='batch-warning')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'api-token-auth', auth_views.obtain_auth_token),
    url(r'api/warnings/active/', views.ActiveBatchWarningsView.as_view(), name='active-warnings'),
    url(r'api/sync/products/(?P<product_id>\w+)', views.ProductsSyncView.as_view(), name='sync-products'),
    url(r'api/sync/batches/', views.ProductBatchSyncView.as_view(), name='sync-batches'),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'dash/', include('dashboard.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', BatchWarningListView.as_view(), name='first-home'),
]
