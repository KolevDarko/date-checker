from django.db import models

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
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    id_code = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class BatchWarning(models.Model):

    STATUS_NEW = 'NEW'
    STATUS_CHECKED = 'CHECKED'

    PRIORITY_WARNING = 'WARNING'
    PRIORITY_EXPIRED = 'EXPIRED'

    product_batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, related_name='batch_warnings')
    status = models.CharField(max_length=10, default=STATUS_NEW)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField(null=True, blank=True)
    priority = models.CharField(max_length=10, default=PRIORITY_WARNING)

    @classmethod
    def generate_warnings(cls):
        all_warnings = cls.objects.raw("select pb.id as id, pb.quantity as old_quantity, pb.expiration_date as expiration_date, pb.product_id "
                                   "from api_productbatch as pb join api_productreminder as remind on "
                                   "pb.product_id=remind.product_id where pb.expiration_date = current_date + remind.days * INTERVAL '1 day' ")
        for data in all_warnings:
            batch_warning = cls(
                product_batch_id=data.id,
                old_quantity=data.old_quantity
            )
            batch_warning.save()
            print("Warning for batch {}, product {}".format(data.id, data.product_id))
