from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from api.models import ProductBatch, Product
from dashboard.forms import ProductForm


class AddProduct(LoginRequiredMixin, generic.CreateView):

    model = Product

    def get(self, request, *args):
        return render(request, 'dashboard/product-add.html', {})

    def render_success(self):
        product_name = self.request.POST['name']
        context = {
            'message': 'Производот {} е снимен'.format(product_name)
        }
        return render(self.request, 'dashboard/product-add.html', context)

    def company_id(self):
        user = self.request.user
        company = user.user_companies.first()
        return company.id

    def post(self, request, *args):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.instance
            new_product.company_id = self.company_id()
            product_form.save()
            return self.render_success()
        else:
            return render(request, 'dashboard/product-add.html', {
                'errors': product_form.errors
            })


class HomeView(LoginRequiredMixin, generic.ListView):

    model = ProductBatch

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/home.html', {})

class ExpirationWarning(LoginRequiredMixin, generic.ListView):

    def get(self, *args):
        pass
