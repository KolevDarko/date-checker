from django.forms.models import ModelForm

from api.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'id_code']
