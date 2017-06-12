from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreatedView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['upc', 'product_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user.credentials
        return super(ProductCreatedView, self).form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['upc', 'product_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user.credentials
        return super(ProductUpdateView, self).form_valid(form)
