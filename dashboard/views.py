from django.shortcuts import render
from django.views import generic

from api.models import ProductInStore, Product
from dashboard.forms import ProductForm


class AddProduct(generic.CreateView):

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
        return user.company_id

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



class HomeView(generic.ListView):

    model = ProductInStore

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/home.html', {})
