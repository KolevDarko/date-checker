from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from api.filters import ProductBatchFilter, ProductFilter
from api.models import Product, Store, ProductBatch, ProductReminder
from dashboard.forms import ProductForm, ProductBatchForm

PRODUCT_REMINDERS = 31

class AddProductView(LoginRequiredMixin, generic.CreateView):

    model = Product

    def get(self, request, *args):
        return render(request, 'dashboard/product-add.html', {'reminder_options': Product.reminders_range()})

    def render_success(self):
        product_name = self.request.POST['name']
        context = {
            'message': 'Производот {} е снимен'.format(product_name),
            'reminder_options': range(2, Product.REMINDER_OPTIONS)
        }
        return render(self.request, 'dashboard/product-add.html', context)

    def create_reminders(self, product):
        for reminder_day in self.request.POST.getlist('reminders'):
            ProductReminder.create_one(reminder_day, product.id)
            print(f"Created {reminder_day}day reminder, for product {product.name} {product.id}")

    def post(self, request, *args):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.instance
            new_product.company_id = self.request.user.company_id
            product_form.save()
            self.create_reminders(new_product)
            return self.render_success()
        else:
            return render(request, 'dashboard/product-add.html', {
                'errors': product_form.errors
            })


class ProductBatchListView(LoginRequiredMixin, generic.ListView):
    filterset_class = ProductBatchFilter
    model = ProductBatch
    template_name = 'dashboard/product-batch-list.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = ProductBatch.objects.filter(product__company_id=self.request.user.company_id).order_by('expiration_date')
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductBatchListView, self).get_context_data(object_list=None, **kwargs)
        context['store_list'] = Store.by_company(self.request.user.company_id)
        context['product_list'] = Product.by_company(self.request.user.company_id)
        context['filterset'] = self.filterset
        return context

    # def get(self, request, *args, **kwargs):
    #     super(ProductBatchListView, self).get(request)

class ProductListView(LoginRequiredMixin, generic.ListView):
    filterset_class = ProductFilter
    model = Product
    template_name = 'dashboard/product-list.html'
    paginate_by = 30

    def get_queryset(self):
        return Product.objects.filter(company_id=self.request.user.company_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(object_list=None, **kwargs)
        context['product_list'] = Product.by_company(self.request.user.company_id)
        return context

class CompanyHomeView(LoginRequiredMixin, generic.ListView):

    model = Store

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/home.html', {})

class ExpirationWarning(LoginRequiredMixin, generic.ListView):

    def get(self, *args):
        # todo finish, show warnings in table sorted decreasing
        pass

class ProductBatchAddView(LoginRequiredMixin, generic.CreateView):

    model = ProductBatch
    form_class = ProductBatchForm
    template_name = 'dashboard/product-batch-form.html'

    def get(self, request, *args):
        form = ProductBatchForm(request.user.company_id)
        return render(request, self.template_name, {'form': form, 'title': 'Додај пратка'})

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

class ProductBatchEditView(LoginRequiredMixin, generic.UpdateView):

    model = ProductBatch
    form_class = ProductBatchForm
    template_name = 'dashboard/product-batch-form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductBatchForm(request.user.company_id, instance=self.object)
        return render(request, self.template_name, {'form': form, 'title': 'Промени пратка'})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(request, self.template_name, {'form': form})

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user.company_id, **self.get_form_kwargs())

    def get_success_url(self):
        return '/dash/product-batch-list'

class EditProductView(LoginRequiredMixin, generic.UpdateView):

    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product-add.html'

    def get(self, request, pk):
        product = self.get_object()
        form = ProductForm.from_product(product)
        return render(request, self.template_name, self.create_context(form, product.reminder_list()))

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = ProductForm(request.POST, instance=product)
        new_reminder_list = request.POST.getlist('reminders')
        new_int_reminders = [int(i) for i in new_reminder_list]
        if form.is_valid():
            product = form.save()
            ProductReminder.update_reminders(product.id, new_int_reminders)
            return HttpResponseRedirect(reverse('dash-product-edit', kwargs={'pk': product.id}))
        else:
            errors = form.errors
            return render(request, self.template_name, self.create_context(form, new_int_reminders, errors))

    def create_context(self, the_form, reminders, errors=None, message=None):
        return {'form': the_form, 'reminder_options': Product.reminders_range(),
         'existing_reminders': reminders, 'errors': errors, 'message': message}
