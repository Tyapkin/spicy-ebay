from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import IndexView, ProductCreatedView, GetProductsListView,\
    CsvExportView, CsvImportView, DeleteProductView, download

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name='index'),

    url(r'^product/add/$',
        login_required(ProductCreatedView.as_view()), name='create_product'),

    url(r'^get_products/$',
        GetProductsListView.as_view(), name='get_products_list'),

    url(r'^product/(?P<pk>[0-9]+)/delete/$',
        login_required(DeleteProductView.as_view()), name='delete_product'),

    url(r'^csv_export/$',
        login_required(CsvExportView.as_view()), name='csv_export'),

    url(r'^csv_import/$',
        login_required(CsvImportView.as_view()), name='csv_import'),

    url(r'^download/(?P<path>.+)$', download, name='download')
]
