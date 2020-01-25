from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models import Company, Store


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_employees', null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='store_employees')
