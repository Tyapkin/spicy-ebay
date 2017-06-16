import csv
from datetime import date
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, Http404

from .models import Product
from .ebay import GetProductByUPC, GetSingleItem


class IndexView(TemplateView):
    template_name = 'index.html'


class GetProductsListView(View):

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            queryset = Product.objects.all()
            json_data = serializers.serialize('json', queryset)
            return HttpResponse(json_data, content_type='application/json')
        else:
            raise Http404()


class ProductCreatedView(View):
    success_msg = 'Products with UPC {} are stored in a database. Successfully saved: {}; Missed {}'
    items_added = 0
    items_missed = 0

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            product_by_upc = GetProductByUPC(self.request.user.credentials.app_id)
            single_item = GetSingleItem(self.request.user.credentials.app_id)
            product_id = self.request.POST.get('upc')
            products_list = product_by_upc.get_product(product_id)
            for item in products_list:
                product = single_item.get_product(item['itemId'])
                try:
                    Product.objects.update_or_create(
                        owner=self.request.user.credentials,
                        upc=item['upc'],
                        product_id=product['ItemID'],
                        defaults={
                            'image': product['GalleryURL'],
                            'rating': product['Seller']['FeedbackScore'],
                            'price': product['CurrentPrice']['Value'],
                            'name': product['Title'],
                            'qty': product['Quantity']
                        }
                    )
                    self.items_added += 1
                except Exception as e:
                    # TODO: logging needs
                    self.items_missed += 1
                    continue
            messages.success(self.request, self.success_msg.format(product_id, self.items_added, self.items_missed))
            return redirect(reverse('index'))
        elif self.request.method == 'GET':
            return render(self.request, 'product_form.html', {})


def export_csv(request):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="products_list.csv"'
    writer = csv.writer(resp)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', 'Testing', 'Here`s a quote'])
    return resp


class CsvProcessingView(View):

    csvfile = 'products_list_{}_{}.csv'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(owner=self.request.user.credentials)
        products_ids = [p.product_id for p in products]
        csvfile = self.csvfile.format(self.request.user.credentials, date.today())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(csvfile)
        writer = csv.writer(response)
        for pid in products_ids:
            writer.writerow([pid])
        return response
