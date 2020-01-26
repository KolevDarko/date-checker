from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from api.models import Product, Store, ProductBatch
from dashboard.forms import ProductForm, ProductBatchForm


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

class ProductBatchListView(LoginRequiredMixin, generic.ListView):
    model = ProductBatch
    template_name = 'dashboard/product-batch-list.html'
    paginate_by = 3

    def get_queryset(self):
        return ProductBatch.objects.filter(product__company_id=self.request.user.company_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductBatchListView, self).get_context_data(object_list=None, **kwargs)
        context['store_list'] = Store.by_company(self.request.user.company_id)
        context['product_list'] = Product.by_company(self.request.user.company_id)
        return context

    # def get(self, request, *args, **kwargs):
    #     super(ProductBatchListView, self).get(request)

class ProductListView(LoginRequiredMixin, generic.ListView):

    model = Product
    template_name = 'dashboard/product-list.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(company_id=self.request.user.company_id)

class CompanyHomeView(LoginRequiredMixin, generic.ListView):

    model = Store

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/home.html', {})

class ExpirationWarning(LoginRequiredMixin, generic.ListView):

    def get(self, *args):
        pass

class ProductBatchAddView(LoginRequiredMixin, generic.CreateView):

    model = ProductBatch
    form_class = ProductBatchForm
    template_name = 'dashboard/product-batch-form.html'

    def get(self, request, *args):
        form = ProductBatchForm(request.user.company_id)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args):
        form = self.get_form()
        if form.is_valid():
            form.save()
            new_form = ProductBatchForm(self.request.user.company_id, initial={'store': form.cleaned_data['store'].id,
                                                                               'product': form.cleaned_data['product'].id})
            return render(request, self.template_name, {'form': new_form})
        else:
            return render(request, self.template_name, {'form': form})

    def get_empty_form(self):
        return ProductBatchForm(self.request.user.company_id)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user.company_id, **self.get_form_kwargs())

    def get_success_url(self):
        return '/dash/product-batch-add'
