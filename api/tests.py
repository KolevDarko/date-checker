import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from api.models import Product, ProductBatch, Company, Store, BatchWarning
from my_accounts.models import User


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
            original_quantity=800,
            expiration_date=expiration_1,
            id_code='batch-1',
            store=self.store_1
        )
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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

    def test_sync_batches_to_server(self):
        batches_url = reverse('sync-batches')
        expiration_date = "2020-02-20"
        data = [
            {
                'product': 1,
                'store': 1,
                'quantity': 50,
                'original_quantity': 50,
                'expiration_date': expiration_date,
                'id_code': 'AS123'
            },
            {
                'product': 1,
                'store': 1,
                'quantity': 30,
                'original_quantity': 30,
                'expiration_date': expiration_date,
                'id_code': 'AS101'
            }
        ]
        response = self.client.post(batches_url, content_type='application/json', data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['quantity'], 50)
        self.assertEqual(response.data[1]['quantity'], 30)


class BatchWarningTests(APITestCase):

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
            original_quantity=800,
            expiration_date=expiration_1,
            id_code='batch-1',
            store=self.store_1
        )
        self.warning_1 = BatchWarning.objects.create(
            product_batch=self.batch_1,
            old_quantity=self.batch_1.quantity
        )
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_batch_and_silence_warnings(self):
        batches_url = reverse('sync-batches')
        data = {
            'id': self.batch_1.id,
            'quantity': 0
        }
        response = self.client.put(batches_url, content_type='application/json', data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.warning_1.refresh_from_db()
        self.assertEqual(self.warning_1.new_quantity, 0)
        self.assertEqual(self.warning_1.product_batch, None)
        self.assertEqual(self.warning_1.product_batch_archive_id, 1)

