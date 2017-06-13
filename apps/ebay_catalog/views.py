from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Product
from .ebay import GetProductByUPC, GetSingleItem


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductCreatedView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['upc']
    success_msg = 'Products with UPC {} are stored in a database. Successfully saved: {}; Missed {}'

    def post(self, request, *args, **kwargs):
        success_added = 0
        unsuccess_added = 0
        if request.POST.get('add_button') is not None:
            call = GetProductByUPC(self.request.user.credentials.app_id)
            call2 = GetSingleItem(self.request.user.credentials.app_id)
            product_id = self.request.POST.get('upc')
            product_list = call.get_product(product_id)
            for item in product_list:
                product = call2.get_product(item['itemId'])
                try:
                    Product.objects.create(
                        owner=self.request.user.credentials,
                        upc=item['upc'],
                        product_id=product['ItemID'],
                        image=product['GalleryURL'],
                        rating=product['Seller']['FeedbackScore'],
                        price=product['CurrentPrice']['Value'],
                        name=product['Title'],
                        qty=product['Quantity']
                    )
                    success_added += 1
                except Exception as e:
                    unsuccess_added += 1
                    continue
            self.success_msg = self.success_msg.format(product_id, success_added, unsuccess_added)
            return super(ProductCreatedView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user.credentials
        return super(ProductCreatedView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse('index')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['upc', 'product_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user.credentials
        return super(ProductUpdateView, self).form_valid(form)
