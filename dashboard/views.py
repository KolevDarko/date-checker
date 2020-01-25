from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from api.models import Product, Store
from dashboard.forms import ProductForm


class AddProductView(LoginRequiredMixin, generic.CreateView):

    model = Product

    def get(self, request, *args):
        return render(request, 'dashboard/product-add.html', {})

    def render_success(self):
        product_name = self.request.POST['name']
        context = {
            'message': 'Производот {} е снимен'.format(product_name)
        }
        return render(self.request, 'dashboard/product-add.html', context)

    def post(self, request, *args):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.instance
            new_product.company_id = self.request.user.company_id
            product_form.save()
            return self.render_success()
        else:
            return render(request, 'dashboard/product-add.html', {
                'errors': product_form.errors
            })


class ProductListView(LoginRequiredMixin, generic.ListView):

    model = Product
    template_name = 'dashboard/product-list.html'
    paginate_by = 3

class CompanyHomeView(LoginRequiredMixin, generic.ListView):

    model = Store

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/home.html', {})

class ExpirationWarning(LoginRequiredMixin, generic.ListView):

    def get(self, *args):
        pass
