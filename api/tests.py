from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Product

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

    def test_get_product(self):
        product = Product.objects.create(name='paracetamol', price=12)
        product_url = reverse('product-detail', args=[product.id])
        response = self.client.get(product_url)
        self.assertEqual(response.data['name'], 'paracetamol')
        self.assertEqual(response.data['price'], 12)

class StoreTest(APITestCase):

    def test_create_store(self):
        url = reverse('store-list')
        location = 'Skopska 13'
        data = {'location': location, 'address': 'skopje'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        store_url = response.data['url']
        get_response = self.client.get(store_url)
        self.assertEqual(get_response.data['location'], location)
