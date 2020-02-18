import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Product, ProductBatch, Company, Store


class ProductTests(APITestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(name='Fit Food')
        self.company.refresh_from_db()

    def test_create_product(self):
        """
        Ensure we can create new products
        """
        url = reverse('product-list')
        data = {'name': 'Coca Cola Cherry', 'price': 30, 'id_code': '1021', 'company_id': self.company.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Coca Cola Cherry')
        self.assertEqual(Product.objects.get().price, 30)

    def test_get_product(self):
        product = Product.objects.create(name='paracetamol', price=12, company=self.company, id_code='dare123')
        product_url = reverse('product-detail', args=[product.id])
        response = self.client.get(product_url)
        self.assertEqual(response.data['name'], 'paracetamol')
        self.assertEqual(response.data['price'], 12)

    def test_get_all_products(self):
        response = self.client.get('/api/products/')
        print(response.data)

class ProductBatchTests(APITestCase):

    def setUp(self) -> None:
        self.company = Company.objects.create(name='Fit Food')
        self.store_1 = Store.objects.create(company=self.company, name='Kocani')
        self.product_1 = Product.objects.create(
            company=self.company,
            name="Toblerone",
            price=120,
            id_code='ASDF123'
        )
        expiration_1 = datetime.datetime.now() + datetime.timedelta(days=7)
        self.batch_1 = ProductBatch.objects.create(
            product=self.product_1,
            quantity=800,
            expiration_date=expiration_1,
            id_code='batch-1',
            store=self.store_1
        )

    def test_update_batch_quantity_and_check_warnings(self):
        batch_url = reverse('productbatch-detail', args=[self.batch_1.id])
        new_quantity = 300
        data = {
            'quantity': new_quantity,
        }
        response = self.client.put(batch_url, content_type='application/json', data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.batch_1.refresh_from_db()
        self.assertEqual(self.batch_1.quantity, new_quantity)
