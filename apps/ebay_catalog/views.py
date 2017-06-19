import csv, os
from datetime import date
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, DeleteView
from django.views.generic.base import ContextMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.conf import settings

from .models import Product
from .ebay import GetProductByUPC, GetSingleItem


class IndexView(TemplateView):
    template_name = 'index.html'


class GetProductsListView(View):

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            queryset = Product.objects.filter(owner=self.request.user.credentials)
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


class CsvExportView(View):

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


class CsvImportView(View):

    csvfilename = 'imported_list.csv'
    success_item = 0
    missed_item = 0
    msg = 'CSV successfully imported. Stored to DB: {}; Missed: {}'

    def get(self, request, *args, **kwargs):
        return render(self.request, 'csv_import_form.html', {})

    def post(self, request, *args, **kwargs):
        get_single_item = GetSingleItem(self.request.user.credentials.app_id)
        csvfile = self.request.FILES['csv']
        csv = self.open_and_read_csv(self.handle_upload_file(csvfile))

        for row in csv:
            try:
                item = get_single_item.get_product(row)
                Product.objects.update_or_create(
                    owner=self.request.user.credentials,
                    product_id=item['ItemID'],
                    defaults={
                        'image': item['GalleryURL'],
                        'rating': item['Seller']['FeedbackScore'],
                        'price': item['CurrentPrice']['Value'],
                        'name': item['Title'],
                        'qty': item['Quantity']
                    }
                )
                self.success_item += 1
            except Exception as e:
                print(e)
                self.missed_item += 1
                continue
        messages.success(self.request, self.msg.format(self.success_item, self.missed_item))
        return redirect(reverse('index'))

    def handle_upload_file(self, f):
        csvfilepath = settings.MEDIA_ROOT + '/' + self.csvfilename

        with open(csvfilepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return csvfilepath

    def open_and_read_csv(self, filepath):
        csvreader = None

        try:
            csvfile = open(filepath, newline='')
            csvreader = csv.reader(csvfile, delimiter='\n')
        except IOError:
            raise IOError

        return csvreader


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'product_delete_form.html'
    success_url = reverse_lazy('index')


def download(request, path):
    # TODO: fix it. This not work.
    file_path = settings.DOWNLOADABLE_FILES + '/' + path
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename={}'.format(file_path)
            return response
    else:
        raise Http404
