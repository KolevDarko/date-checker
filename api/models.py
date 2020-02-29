from dateutil.parser import parse
from django.db import models
import datetime


class ModelMixin():

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(pk=id)


class Company(models.Model):
    name = models.CharField(max_length=200)


class Store(models.Model, ModelMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_stores')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def by_company(cls, company_id):
        return cls.objects.filter(company_id=company_id)


class Product(models.Model, ModelMixin):
    REMINDER_OPTIONS = 31
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_products')
    name = models.CharField(max_length=300)
    price = models.FloatField()
    id_code = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.name, self.id_code)

    @classmethod
    def reminders_range(cls):
        return range(1, Product.REMINDER_OPTIONS)

    @classmethod
    def by_company(cls, company_id):
        return cls.objects.filter(company_id=company_id)

    @classmethod
    def products_after(cls, company_id, latest_product_id):
        return cls.objects.filter(company_id=company_id, id__gt=latest_product_id)

    def reminder_list(self):
        return self.reminders.values_list('days', flat=True)


class ProductReminder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reminders')
    days = models.IntegerField(default=7)

    @classmethod
    def create_one(cls, reminder_day, product_id):
        return cls.objects.create(days=reminder_day, product_id=product_id)

    @classmethod
    def update_reminders(cls, product_id, new_reminder_list):
        cls.objects.filter(product_id=product_id).delete()
        for reminder_days in new_reminder_list:
            cls.create_one(reminder_days, product_id)


class ProductBatch(models.Model, ModelMixin):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='store_batches')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_batches')
    original_quantity = models.IntegerField()
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    id_code = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @classmethod
    def create_new(cls, data, store_id):
        return cls.objects.create(
            store_id=store_id,
            product_id=data.product_id,
            original_quantity=data.quantity,
            quantity=data.quantity,
            expiration_data=parse(data.expiration_date),
            id_code=data.id_code
        )

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.save()


class ProductBatchArchive(models.Model, ModelMixin):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='archived_store_batches')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='archived_product_batches')
    batch_id = models.IntegerField()
    original_quantity = models.IntegerField()
    leftover_quantity = models.IntegerField()
    expiration_date = models.DateField()
    id_code = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_batch_archive(cls, batch):
        archive = cls()
        archive.store_id = batch.store_id
        archive.product_id = batch.product_id
        archive.batch_id = batch.id
        archive.original_quantity = batch.original_quantity
        archive.leftover_quantity = batch.quantity
        archive.expiration_date = batch.expiration_date
        archive.id_code = batch.id_code
        archive.save()
        return archive


class BatchWarning(models.Model, ModelMixin):
    STATUS_NEW = 'NEW'
    STATUS_CHECKED = 'CHECKED'

    PRIORITY_WARNING = 'WARNING'
    PRIORITY_EXPIRED = 'EXPIRED'

    product_batch = models.ForeignKey(ProductBatch, on_delete=models.DO_NOTHING, related_name='batch_warnings',
                                      null=True, blank=True)
    product_batch_archive = models.ForeignKey(ProductBatchArchive, on_delete=models.DO_NOTHING,
                                              related_name='batch_warnings', null=True, blank=True)
    status = models.CharField(max_length=10, default=STATUS_NEW)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField(null=True, blank=True)
    priority = models.CharField(max_length=10, default=PRIORITY_WARNING)

    @classmethod
    def generate_all_warnings(cls):
        cls.generate_normal_warnings()
        cls.generate_expired_warnings()

    @classmethod
    def generate_normal_warnings(cls):
        all_warnings = cls.objects.raw(
            "select pb.id as id, pb.quantity as old_quantity, pb.expiration_date as expiration_date, pb.product_id "
            "from api_productbatch as pb join api_productreminder as remind on "
            "pb.product_id=remind.product_id where pb.expiration_date = current_date + remind.days * INTERVAL '1 day' ")
        for data in all_warnings:
            batch_warning = cls(
                product_batch_id=data.id,
                old_quantity=data.old_quantity
            )
            batch_warning.save()
            print("Warning for batch {}, product {}".format(data.id, data.product_id))

    @classmethod
    def generate_expired_warnings(cls):
        expired_batches = ProductBatch.objects.filter(expiration_date__lt=datetime.datetime.utcnow())
        for batch in expired_batches:
            batch_warning = cls(product_batch_id=batch.id, old_quantity=batch.quantity, priority=cls.PRIORITY_EXPIRED)
            batch_warning.save()
            print("Expired warning for batch {}, product {}".format(batch.id, batch.product_id))

    @classmethod
    def silence_warnings(cls, batch_id, new_quantity):
        cls.objects.filter(product_batch_id=batch_id, status=cls.STATUS_NEW).update(
            status=cls.STATUS_CHECKED,
            new_quantity=new_quantity
        )

    @classmethod
    def archive_warnings(cls, batch_id, batch_archive_id):
        cls.objects.filter(product_batch_id=batch_id).update(
            product_batch=None,
            product_batch_archive=batch_archive_id
        )

    @staticmethod
    def calc_days_left(expiration_date):
        return (expiration_date - datetime.datetime.utcnow().date()).days

    @classmethod
    def get_active(cls, store_id):
        active_warnings = cls.objects.filter(product_batch__store_id=store_id, status=cls.STATUS_NEW).select_related(
            'product_batch', 'product_batch__product').order_by('product_batch__expiration_date')
        results = []
        for warning in active_warnings:
            results.append({
                "id": warning.id,
                "product_batch_id": warning.product_batch_id,
                "expiration_date": warning.product_batch.expiration_date,
                "days_left": cls.calc_days_left(warning.product_batch.expiration_date),
                "product_id": warning.product_batch.product_id,
                "product_name": warning.product_batch.product.name,
                "quantity": warning.product_batch.quantity,
                "priority": warning.priority
            })
        return results

    def mark_checked(self, new_quantity):
        self.new_quantity = new_quantity
        self.status = self.STATUS_CHECKED
        self.save()
