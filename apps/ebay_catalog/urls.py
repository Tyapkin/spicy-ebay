from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import IndexView, ProductCreatedView, GetProductsListView, CsvProcessingView

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name='index'),

    url(r'^product/add/$',
        login_required(ProductCreatedView.as_view()), name='create_product'),

    url(r'^get_products/$',
        GetProductsListView.as_view(), name='get_products_list'),

    url(r'^csv_processing/$',
        login_required(CsvProcessingView.as_view()), name='csv_processing'),
]
