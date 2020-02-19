from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from api.models import Company, Store

@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_employees', null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='store_employees')
