from django import forms
from django.forms.models import ModelForm

from api.models import Product, ProductBatch, Store


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'id_code']

    @classmethod
    def from_product(cls, product):
        return cls({'name': product.name, 'price': product.price, 'id_code': product.id_code})

class ProductBatchForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = ['store', 'product', 'quantity', 'expiration_date', 'id_code']

    def __init__(self, company_id, *args, **kwargs):
        super(ProductBatchForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(company_id=company_id)
        self.fields['store'].queryset = Store.objects.filter(company_id=company_id)
