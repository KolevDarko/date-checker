from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic

from api.models import ProductInStore


class HomeView(View):

    def get(self, request):
        return render(request, 'dashboard/home.html', {})


class AddProduct(LoginRequiredMixin, generic.CreateView):

    def get(self, request):
        pass


class ProductList(LoginRequiredMixin, generic.ListView):

    model = ProductInStore

    def get(self, request, *args, **kwargs):
        pass
