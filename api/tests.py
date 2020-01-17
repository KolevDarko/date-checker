from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Product, ProductInStore, Store

class ProductTests(APITestCase):
    def test_create_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        data = {'name': 'Coca Cola Cherry', 'price': 30}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Coca Cola Cherry')
        self.assertEqual(Product.objects.get().price, 30)
