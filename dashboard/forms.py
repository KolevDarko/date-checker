from django import forms
from django.forms.models import ModelForm

from api.models import Product, ProductBatch, Store


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'id_code']

class ProductBatchForm(forms.Form):
    # name = forms.CharField(max_length=100)
    # authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
    # store = forms.ModelChoiceField(queryset=Store.objects.all())
    class Meta:
        model = ProductBatch
        fields = ['store', 'product', 'quantity', 'expiration_date', 'id_code']
